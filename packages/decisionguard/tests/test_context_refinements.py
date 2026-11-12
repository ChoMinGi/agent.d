import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/decisionguard/scripts"))
from decisionguard import ValidationError, load_json
from context_prepare import prepare_context
from raw_context import build_job, compile_extraction, load_bundle, prepare_raw


class ContextRefinementTests(unittest.TestCase):
    def setUp(self):
        demo = ROOT / "examples/lantern-docs"
        self.snapshot = load_json(demo / "context-snapshot.json")
        self.task = load_json(demo / "requests/feature_design.json")

    def record(self, rid):
        return next(r for r in self.snapshot["context_records"] if r["id"] == rid)

    def source(self, rid):
        row = self.record(rid)
        return next(s for s in self.snapshot["sources"] if s["id"] == row["source_id"])

    def test_bounded_observation_keeps_missing_source_context_visible(self):
        self.task["type"] = "market_research"
        source = self.source("E-MARKET")
        source["content"] += "\nThe export stops before the price comparison."
        source["complete"] = False
        self.record("E-MARKET")["partial_context"] = {
            "boundary_quote": "The export stops before the price comparison.",
            "rationale": "Only the visible interface observation is available; prices are unknown."}
        packet = prepare_context(self.snapshot, self.task)
        selected = next(r for r in packet["selected"] if r["id"] == "E-MARKET")
        self.assertFalse(selected["source_complete"])
        self.assertTrue(selected["partial_context"])
        self.assertEqual(packet["status"], "needs_context")
        self.assertTrue(any("bounded excerpt" in gap for gap in packet["gaps"]))

    def test_partial_excerpt_cannot_establish_design_authority(self):
        self.source("A-01")["complete"] = False
        self.record("A-01")["partial_context"] = {
            "boundary_quote": self.record("A-01")["quote"], "rationale": "A partial export."}
        with self.assertRaisesRegex(ValidationError, "never authority"):
            prepare_context(self.snapshot, self.task)

    def test_task_relevance_can_include_a_useful_kind_outside_default_profile(self):
        self.task["relevance"] = [
            {"record_id": "E-MARKET", "action": "include", "rationale": "Compare the demonstrated interface pattern for this design."},
            {"record_id": "E-CUST", "action": "exclude", "rationale": "The supplied request concerns the interface comparison only."}]
        packet = prepare_context(self.snapshot, self.task)
        chosen = {r["id"] for r in packet["selected"]}
        self.assertIn("E-MARKET", chosen)
        self.assertNotIn("E-CUST", chosen)

    def test_relevance_never_bypasses_project_scope_or_inactive_status(self):
        self.task["relevance"] = [{"record_id": rid, "action": "include", "rationale": "Attempt to force this record."}
                                  for rid in ["E-OTHER", "R-ENT", "D-007"]]
        chosen = {r["id"] for r in prepare_context(self.snapshot, self.task)["selected"]}
        self.assertFalse(chosen & {"E-OTHER", "R-ENT", "D-007"})

    def test_excluding_competing_accepted_decision_does_not_hide_conflict(self):
        next(r for r in self.snapshot["decisions"] if r["id"] == "D-060")["status"] = "accepted"
        self.task["relevance"] = [{"record_id": "D-060", "action": "exclude", "rationale": "Not useful to the requested work."}]
        packet = prepare_context(self.snapshot, self.task)
        self.assertTrue(packet["conflicts"])
        self.assertIn("D-060", packet["conflicts"][0]["record_ids"])

    def test_cited_dependency_overrides_exclusion_with_disclosure(self):
        self.task["relevance"] = [{"record_id": "K-RACE", "action": "exclude", "rationale": "Different topic."}]
        packet = prepare_context(self.snapshot, self.task)
        self.assertIn("K-RACE", {r["id"] for r in packet["selected"]})
        self.assertTrue(any("overrides its task exclusion" in g for g in packet["gaps"]))

    def test_planned_cases_are_known_context_without_becoming_test_results(self):
        self.task["type"] = "qa_review"
        self.record("T-01")["status"] = "planned"
        packet = prepare_context(self.snapshot, self.task)
        record = next(r for r in packet["selected"] if r["id"] == "T-01")
        self.assertEqual((record["kind"], record["status"]), ("test_case", "planned"))
        self.assertFalse(any("Missing supported test_case" in g for g in packet["gaps"]))
        self.assertTrue(any("not an executed result" in c for c in packet["cautions"]))

    def test_missing_design_label_is_not_equated_with_missing_implementation(self):
        self.record("A-01")["kind"] = "requirement"
        packet = prepare_context(self.snapshot, self.task)
        self.assertFalse(any("Missing supported design" in g for g in packet["gaps"]))
        self.assertTrue(any("Classification alone" in c for c in packet["cautions"]))
        self.assertIn("A-01", {r["id"] for r in packet["selected"]})
        self.assertEqual(len(packet["selected"]), len({r["id"] for r in packet["selected"]}))

    def test_without_any_accepted_design_alternative_a_gap_remains(self):
        self.snapshot["decisions"] = []
        self.snapshot["impacts"] = []
        self.snapshot["context_links"] = []
        for row in self.snapshot["context_records"]:
            if row["kind"] in {"design", "requirement"}:
                row["status"] = "unknown"
        packet = prepare_context(self.snapshot, self.task)
        self.assertTrue(any("Missing supported design" in g for g in packet["gaps"]))


class RawRefinementTests(unittest.TestCase):
    def setUp(self):
        demo = ROOT / "examples/morrow-rooms"
        self.job = build_job(load_bundle(demo / "documents.json"), load_json(demo / "requests.json"))
        self.response = load_json(demo / "recorded-extraction.json")

    def test_cross_document_rejection_preserves_both_citations(self):
        # R07 is a proposal; use another supplied passage to exercise grounding
        # mechanics. Whether it actually rejects the proposal remains model review.
        row = next(r for r in self.response["records"] if r["id"] == "R07")
        other = next(r for r in self.response["records"] if r["id"] == "R02")
        row.update(status="rejected", status_evidence=copy.deepcopy(other["evidence"]),
                   status_link=copy.deepcopy(other["evidence"]), status_rationale="This is the explicit disposition of the earlier proposal.")
        snapshot, _, annotations = compile_extraction(self.job, self.response)
        normalized = next(r for r in snapshot["decisions"] if r["id"] == "R07")
        self.assertEqual(normalized["source_id"], "note-03")
        self.assertEqual(normalized["status_source_id"], "note-01")
        self.assertTrue(annotations["R07"]["status_link"])
        self.assertNotIn("R07", {r["id"] for r in prepare_raw(self.job, self.response)["research"]["selected"]})

    def test_relevance_requires_accounting_for_all_extracted_records(self):
        self.response["task_interpretations"][0]["relevance"] = []
        with self.assertRaisesRegex(ValidationError, "every extracted record"):
            prepare_raw(self.job, self.response)

    def test_unverified_cross_document_authority_cannot_be_borrowed(self):
        row = self.response["records"][0]
        row["status_evidence"] = copy.deepcopy(self.response["records"][3]["evidence"])
        with self.assertRaisesRegex(ValidationError, "explicit status_link"):
            prepare_raw(self.job, self.response)

    def test_unavailable_separate_authority_is_not_used_as_accepted(self):
        row = self.response["records"][0]
        other = self.response["records"][3]
        row.update(status_evidence=copy.deepcopy(other["evidence"]), status_link=copy.deepcopy(other["evidence"]),
                   status_rationale="Separate approval for this goal.")
        snapshot, tasks, _ = compile_extraction(self.job, self.response)
        next(s for s in snapshot["sources"] if s["id"] == "note-02")["complete"] = False
        packet = prepare_context(snapshot, tasks["research"])
        self.assertNotIn("R01", {r["id"] for r in packet["selected"]})
        self.assertTrue(any("status authority source is incomplete" in g for g in packet["gaps"]))


if __name__ == "__main__":
    unittest.main()

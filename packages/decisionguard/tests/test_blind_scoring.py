import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from score_context_packets import score_packets


class BlindScoringTests(unittest.TestCase):
    def setUp(self):
        self.answers = {"suite": "synthetic-scoring-contract", "cases": [{"request_id": "q", "type": "qa_review"}],
                        "facts": [
                            {"id": "required", "source_id": "s", "quote_contains": "The run failed.",
                             "acceptable_kinds": ["test_result"], "status": "observed", "required_for": ["q"], "allowed_for": ["q"]},
                            {"id": "optional", "source_id": "s", "quote_contains": "We approved the boundary.",
                             "acceptable_kinds": ["decision", "requirement"], "status": "accepted", "required_for": [], "allowed_for": ["q"]},
                            {"id": "unrelated", "source_id": "s", "quote_contains": "Office snacks arrived.",
                             "acceptable_kinds": ["task"], "status": "done", "required_for": [], "allowed_for": []}]}
        self.packets = {"q": {"task": {"type": "qa_review"}, "status": "context_prepared", "gaps": [],
                              "selected": [{"id": "r", "kind": "test_result", "status": "observed",
                                            "evidence": {"id": "s", "quote": "The run failed."}}]}}

    def test_missing_required_fact_is_counted_without_default_credit(self):
        self.packets["q"]["selected"] = []
        result = score_packets(self.packets, self.answers)
        self.assertFalse(result["passed"])
        self.assertEqual(result["cases"][0]["missing_required"], ["required"])

    def test_optional_context_and_alternative_valid_kind_are_allowed(self):
        self.packets["q"]["selected"].append({"id": "o", "kind": "requirement", "status": "accepted",
                                               "evidence": {"id": "s", "quote": "We approved the boundary."}})
        self.assertTrue(score_packets(self.packets, self.answers)["passed"])

    def test_wrong_context_and_wrong_status_are_reported_separately(self):
        self.packets["q"]["selected"][0]["status"] = "accepted"
        self.packets["q"]["selected"].append({"id": "x", "kind": "task", "status": "done",
                                               "evidence": {"id": "s", "quote": "Office snacks arrived."}})
        case = score_packets(self.packets, self.answers)["cases"][0]
        self.assertEqual(case["required_covered"], 1)
        self.assertEqual(case["classification_errors"][0]["fields"], ["status"])
        self.assertEqual(case["wrong_context"][0]["fact_ids"], ["unrelated"])

    def test_source_mismatch_is_not_a_fact_match(self):
        self.packets["q"]["selected"][0]["evidence"]["id"] = "other-project"
        case = score_packets(self.packets, self.answers)["cases"][0]
        self.assertEqual(case["missing_required"], ["required"])
        self.assertEqual(case["unmatched_records_for_review"], ["r"])

    def test_scoring_does_not_modify_sealed_data(self):
        before = copy.deepcopy((self.packets, self.answers))
        self.assertTrue(score_packets(self.packets, self.answers)["passed"])
        self.assertEqual((self.packets, self.answers), before)


if __name__ == "__main__":
    unittest.main()

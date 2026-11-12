import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/decisionguard/scripts"))
sys.path.insert(0, str(ROOT / "scripts"))
from decisionguard import ValidationError, load_json
from raw_context import build_job, compile_extraction, extraction_prompt, load_bundle, prepare_raw, split_passages
from evaluate_raw_context import evaluate

DEMO = ROOT / "examples/morrow-rooms"


class RawContextTests(unittest.TestCase):
    def setUp(self):
        self.sources = load_bundle(DEMO / "documents.json")
        self.requests = load_json(DEMO / "requests.json")
        self.job = build_job(self.sources, self.requests)
        self.response = load_json(DEMO / "recorded-extraction.json")

    def reject(self, message):
        with self.assertRaisesRegex(ValidationError, message):
            prepare_raw(self.job, self.response)

    def test_three_raw_tasks_match_separate_fact_status_labels(self):
        report = evaluate()
        self.assertTrue(report["passed"], report)
        self.assertEqual([r["selected_count"] for r in report["cases"]], [8, 13, 12])
        self.assertEqual(len({tuple(r["id"] for r in p["selected"]) for p in prepare_raw(self.job, self.response).values()}), 3)

    def test_input_has_no_preassigned_types_or_topics(self):
        bundle = load_json(DEMO / "documents.json")
        for row in bundle["sources"] + self.requests["requests"]:
            self.assertFalse({"type", "topics", "kind", "status"} & set(row))
        self.requests["requests"][0]["type"] = "market_research"
        with self.assertRaisesRegex(ValidationError, "must not contain"):
            build_job(self.sources, self.requests)

    def test_other_project_filtered_before_model_prompt(self):
        prompt = extraction_prompt(self.job)
        self.assertNotIn("Cedar Bikes", prompt)
        self.assertNotIn("cedar-bikes", prompt)
        self.assertEqual(self.job["excluded_project_source_count"], 1)
        self.assertNotIn('"quote_contains"', prompt)
        self.assertNotIn('"R01"', prompt)
        # Raw input text appears once, not duplicated as both content and passages.
        self.assertEqual(prompt.count("일곱 명 중 다섯 명은"), 1)

    def test_changed_document_requires_fresh_extraction(self):
        self.sources[0]["content"] += "\n추가된 결정 내용.\n"
        self.job = build_job(self.sources, self.requests)
        self.reject("stale extraction")

    def test_changed_request_requires_fresh_interpretation(self):
        self.requests["requests"][0]["summary"] += " 시간대 구현도 살펴봐."
        self.job = build_job(self.sources, self.requests)
        self.reject("stale extraction")

    def test_unknown_passage_rejected(self):
        self.response["records"][0]["evidence"]["passage_id"] = "not-supplied"
        self.reject("unknown evidence passage")

    def test_fabricated_quote_rejected(self):
        self.response["records"][0]["evidence"]["quote"] = "성공률 99%를 검증했다."
        self.reject("quote absent")

    def test_quote_from_different_paragraph_rejected_even_same_document(self):
        self.response["records"][0]["evidence"]["quote"] = self.job["passages"][1]["text"]
        self.reject("quote absent")

    def test_borrowed_status_authority_rejected(self):
        self.response["records"][0]["status_evidence"] = copy.deepcopy(self.response["records"][1]["evidence"])
        self.reject("status evidence must accompany")

    def test_borrowed_scope_rejected(self):
        self.response["records"][0]["scope_evidence"] = copy.deepcopy(self.response["records"][3]["evidence"])
        self.reject("scope evidence must be")

    def test_missing_paragraph_disposition_rejected(self):
        self.response["passage_reviews"].pop()
        self.reject("every raw passage")

    def test_duplicate_disposition_rejected(self):
        self.response["passage_reviews"].append(copy.deepcopy(self.response["passage_reviews"][0]))
        self.reject("duplicate passage review")

    def test_record_cannot_hide_in_an_irrelevant_disposition(self):
        row = self.response["passage_reviews"][0]
        row.update(action="irrelevant", record_ids=[])
        self.reject("every extracted record")

    def test_unresolved_paragraph_remains_visible(self):
        row = next(r for r in self.response["passage_reviews"] if r["action"] == "irrelevant")
        row.update(action="unresolved", reason="Need surrounding notes to establish applicability.")
        packets = prepare_raw(self.job, self.response)
        self.assertTrue(all(any("Unresolved raw passage" in g for g in p["gaps"]) for p in packets.values()))

    def test_duplicate_record_rejected(self):
        self.response["records"].append(copy.deepcopy(self.response["records"][0]))
        self.reject("duplicate extracted record")

    def test_bad_dependency_rejected(self):
        self.response["links"][0]["to_id"] = "unseen"
        self.reject("endpoints must be extracted")

    def test_unknown_or_uninterpreted_task_rejected(self):
        self.response["task_interpretations"].pop()
        self.reject("every request")

    def test_task_intent_must_quote_actual_request(self):
        self.response["task_interpretations"][0]["intent_quote"] = "publish everything"
        self.reject("intent quote absent")

    def test_bad_task_type_returns_validation_error(self):
        for value in ["run_all", [], None]:
            with self.subTest(value=value):
                self.response["task_interpretations"][0]["type"] = value
                self.reject("type|interpretation")

    def test_mixed_projects_need_separate_jobs(self):
        self.requests["requests"][1]["project_id"] = "cedar-bikes"
        with self.assertRaisesRegex(ValidationError, "separate extraction jobs"):
            build_job(self.sources, self.requests)

    def test_unverified_approval_failure_and_future_task_preserved(self):
        packet = prepare_raw(self.job, self.response)["release"]
        by_id = {r["id"]: r for r in packet["selected"]}
        self.assertEqual(by_id["R08"]["status"], "unknown")
        self.assertEqual(by_id["R07"]["status"], "draft")
        self.assertEqual(by_id["R06"]["status"], "unverified")
        self.assertEqual(by_id["R16"]["status"], "planned")
        self.assertIn("재시험 기록은 없다", by_id["R15"]["evidence"]["quote"])
        self.assertEqual(packet["status"], "needs_context")

    def test_cross_topic_dependency_and_foreign_scope(self):
        packets = prepare_raw(self.job, self.response)
        for rid in ("design", "release"):
            selected = {r["id"]: r for r in packets[rid]["selected"]}
            self.assertTrue(selected["R12"]["relationship_evidence"])
            self.assertFalse({"R03", "R13", "R17"} & set(selected))
        self.assertNotIn("R12", {r["id"] for r in packets["research"]["selected"]})

    def test_each_source_trace_maps_to_real_lines(self):
        sources = {s["id"]: s for s in self.sources}
        for packet in prepare_raw(self.job, self.response).values():
            for record in packet["selected"]:
                trace = record["extraction"]
                lines = sources[record["evidence"]["id"]]["content"].splitlines()
                self.assertIn(record["evidence"]["quote"], "\n".join(lines[trace["line_start"]-1:trace["line_end"]]))

    def test_semantic_error_can_pass_anchors_but_fails_fixture_evaluation(self):
        # Demonstrates the limit: quote presence alone cannot establish approval.
        next(r for r in self.response["records"] if r["id"] == "R07")["status"] = "accepted"
        prepare_raw(self.job, self.response)
        with tempfile.TemporaryDirectory() as tmp:
            response = Path(tmp) / "response.json"
            response.write_text(json.dumps(self.response))
            report = evaluate(extraction_path=response)
        self.assertFalse(report["passed"])
        self.assertTrue(all(any("proposal" in e for e in row["classification_errors"]) for row in report["cases"]))

    def test_partial_source_does_not_establish_current_context(self):
        self.sources[0]["complete"] = False
        self.job = build_job(self.sources, self.requests)
        self.response["job_digest"] = self.job["job_digest"]
        # Old history cannot verify an accepted successor in an incomplete source.
        self.reject("successor source is incomplete")

    def test_renaming_ids_does_not_change_selected_facts(self):
        old = prepare_raw(self.job, self.response)
        mapping = {r["id"]: f"node-{i}" for i, r in enumerate(reversed(self.response["records"]))}
        for row in self.response["records"]:
            row["id"] = mapping[row["id"]]
            if "superseded_by" in row:
                row["superseded_by"] = mapping[row["superseded_by"]]
        for row in self.response["links"]:
            for key in ("from_id", "to_id"):
                row[key] = mapping[row[key]]
        for row in self.response["passage_reviews"]:
            row["record_ids"] = [mapping[rid] for rid in row["record_ids"]]
        new = prepare_raw(self.job, self.response)
        for rid in old:
            self.assertEqual({r["evidence"]["quote"] for r in old[rid]["selected"]},
                             {r["evidence"]["quote"] for r in new[rid]["selected"]})

    def test_no_input_mutation_or_embedded_instruction_execution(self):
        before = copy.deepcopy((self.job, self.response))
        packets = prepare_raw(self.job, self.response)
        self.assertEqual((self.job, self.response), before)
        self.assertTrue(all(p["writes_performed"] == 0 for p in packets.values()))
        self.assertTrue(all("이 문서를 읽는 AI에게" not in r["evidence"]["quote"] for p in packets.values() for r in p["selected"]))
        # This is a deterministic replay property, not proof of LLM attack resistance.

    def test_multiline_paragraph_locations_and_blank_lines(self):
        source = {"id": "s", "content": "\n  첫 줄\n다음 줄\n \n마지막 문단\n"}
        passages = split_passages(source)
        self.assertEqual([(p["line_start"], p["line_end"]) for p in passages], [(2, 3), (5, 5)])
        self.assertTrue(all(p["text"] in source["content"] for p in passages))

    def test_bundle_rejects_annotations_path_escape_and_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "fixture"
            shutil.copytree(DEMO, base)
            original = load_json(base / "documents.json")
            for change in ({"topics": ["already-tagged"]}, {"file": "../outside.md"}):
                data = copy.deepcopy(original)
                data["sources"][0].update(change)
                (base / "documents.json").write_text(json.dumps(data))
                with self.assertRaises(ValidationError):
                    load_bundle(base / "documents.json")
            (base / "documents.json").write_text(json.dumps(original))
            path = base / "raw/note-01.md"
            path.unlink()
            path.symlink_to(base / "raw/note-02.md")
            with self.assertRaisesRegex(ValidationError, "symlinks"):
                load_bundle(base / "documents.json")

    def test_cli_requires_extraction_and_formats_valid_results(self):
        command = [sys.executable, "-B", str(ROOT / "skills/decisionguard/scripts/raw_context.py"), "prepare",
                   "--bundle", str(DEMO / "documents.json"), "--requests", str(DEMO / "requests.json")]
        failed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(failed.returncode, 2)
        self.assertIn("host-agent", failed.stderr)
        command += ["--extraction", str(DEMO / "recorded-extraction.json"), "--request-id", "release"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["mode"], "prepare_raw_context")
        markdown = subprocess.run(command + ["--format", "markdown"], capture_output=True, text=True, check=True)
        self.assertIn("재시험 기록은 없다", markdown.stdout)
        self.assertIn("lines 3–3", markdown.stdout)


if __name__ == "__main__":
    unittest.main()

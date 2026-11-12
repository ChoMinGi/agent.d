#!/usr/bin/env python3
"""Evaluate a recorded host extraction against separate fictional fact labels.

No model is called. Use --extraction to score a fresh host response to the same
job; keep expectations.json hidden from that extraction session.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/decisionguard/scripts"))
from decisionguard import load_json
from raw_context import build_job, load_bundle, prepare_raw, render_raw


def evaluate(output_dir=None, extraction_path=None):
    demo = ROOT / "examples/morrow-rooms"
    job = build_job(load_bundle(demo / "documents.json"), load_json(demo / "requests.json"))
    response = load_json(extraction_path or demo / "recorded-extraction.json")
    packets = prepare_raw(job, response)
    labels = load_json(demo / "expectations.json")
    reports = []
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    for case in labels["cases"]:
        rid = case["request_id"]
        packet = packets[rid]
        expected = {f["name"]: f for f in labels["facts"] if rid in f["requests"]}
        found, unexpected, errors, forbidden = set(), [], [], []
        for record in packet["selected"]:
            evidence = record["evidence"]
            matching = [f for f in expected.values() if f["source_id"] == evidence["id"]
                        and f["quote_contains"] in evidence["quote"]]
            if not matching:
                unexpected.append(record["id"])
            for fact in matching:
                if fact["name"] in found:
                    errors.append(f"Duplicate selected fact: {fact['name']}")
                found.add(fact["name"])
                for field in ("kind", "status"):
                    if record[field] != fact[field]:
                        errors.append(f"{fact['name']}: expected {field}={fact[field]}, got {record[field]}")
            forbidden.extend(fragment for fragment in labels["forbidden_quote_fragments"]
                             if fragment in evidence["quote"])
        missing = sorted(set(expected) - found)
        if packet["task"]["type"] != case["type"]:
            errors.append("Wrong task interpretation")
        if packet["status"] != case["status"]:
            errors.append("Wrong context readiness state")
        passed = not missing and not unexpected and not errors and not forbidden and packet["writes_performed"] == 0
        reports.append({"request_id": rid, "task_type": packet["task"]["type"], "passed": passed,
                        "expected_facts": len(expected), "matched_facts": len(found),
                        "selected_count": len(packet["selected"]), "missing_facts": missing,
                        "unexpected_records": unexpected, "classification_errors": errors,
                        "forbidden_selected": forbidden, "status": packet["status"],
                        "gaps": packet["gaps"], "writes_performed": packet["writes_performed"]})
        if output_dir is not None:
            (output_dir / f"{rid}.md").write_text(render_raw(packet), encoding="utf-8")
            (output_dir / f"{rid}.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {"release": "0.3.0", "dataset": "fictional Morrow Rooms: untagged Korean/English prose",
              "method": "replay of one host-agent extraction; deterministic fact-anchor and interpretation-label checks",
              "passed": all(r["passed"] for r in reports), "cases": reports,
              "input_documents": len(job["sources"]), "input_passages": len(job["passages"]),
              "excluded_other_project_documents": job["excluded_project_source_count"],
              "limits": ["Same author created corpus, expectations, extraction and implementation; no independent benchmark.",
                         "The CLI does not run a language model. This replay does not measure fresh extraction reliability.",
                         "Fact anchors and status labels are fixture-specific; excerpt presence alone cannot prove semantic entailment.",
                         "No live Notion retrieval/write, broad language coverage or adversarial LLM robustness was measured."]}
    if output_dir is not None:
        (output_dir / "evaluation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--extraction", type=Path, help="Optional fresh response to the unchanged fictional job")
    args = parser.parse_args()
    report = evaluate(args.output_dir, args.extraction)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report["passed"] else 1)

#!/usr/bin/env python3
"""Score sealed context packets against separately authored fictional fact labels.

This is a deterministic audit aid, not a semantic judge or an extraction runner.
Freeze inputs/answers before extracting; reveal answers only after sealing output.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/decisionguard/scripts"))
from decisionguard import load_json, require


def matches(record, fact):
    evidence = record["evidence"]
    return evidence["id"] == fact["source_id"] and fact["quote_contains"] in evidence["quote"]


def score_packets(packets, answers):
    facts = answers["facts"]
    require(len({f["id"] for f in facts}) == len(facts), "duplicate answer fact ID")
    cases = []
    for case in answers["cases"]:
        rid = case["request_id"]
        require(rid in packets, "missing request packet")
        packet = packets[rid]
        required = {f["id"] for f in facts if rid in f["required_for"]}
        covered, wrong_context, unmatched, classifications = set(), [], [], []
        for record in packet["selected"]:
            matched = [f for f in facts if matches(record, f)]
            allowed = [f for f in matched if rid in f["allowed_for"]]
            forbidden = [f for f in matched if rid not in f["allowed_for"]]
            if not matched:
                unmatched.append(record["id"])
            elif not allowed:
                wrong_context.append({"record_id": record["id"], "fact_ids": [f["id"] for f in forbidden]})
            covered.update(f["id"] for f in allowed)
        # One paragraph may support several records. Score each fact once, using
        # a compatible interpretation when available, rather than penalizing all
        # the other records that happen to quote the same surrounding paragraph.
        for fact in facts:
            if rid not in fact["allowed_for"]:
                continue
            matching = [r for r in packet["selected"] if matches(r, fact)]
            if not matching:
                continue
            compatible = [r for r in matching if r["kind"] in fact["acceptable_kinds"]]
            exact = [r for r in compatible if r["status"] == fact["status"]]
            if exact:
                continue
            record = (compatible or matching)[0]
            errors = ([] if compatible else ["kind"]) + ([] if record["status"] == fact["status"] else ["status"])
            classifications.append({"record_id": record["id"], "fact_id": fact["id"], "fields": errors,
                                    "actual_kind": record["kind"], "actual_status": record["status"],
                                    "allowed_kinds": fact["acceptable_kinds"], "expected_status": fact["status"]})
        missing = sorted(required - covered)
        correct_type = packet["task"]["type"] == case["type"]
        cases.append({"request_id": rid, "task_type": packet["task"]["type"],
                      "required_count": len(required), "required_covered": len(required & covered),
                      "missing_required": missing, "selected_count": len(packet["selected"]),
                      "wrong_context": wrong_context, "unmatched_records_for_review": unmatched,
                      "classification_errors": classifications, "task_type_correct": correct_type,
                      "packet_status": packet["status"], "gaps": packet["gaps"],
                      "passed": not missing and not wrong_context and not unmatched and not classifications and correct_type})
    return {"suite": answers["suite"], "passed": all(c["passed"] for c in cases), "cases": cases,
            "limits": ["Exact fact anchors may miss a valid shorter paraphrase/quote; inspect every flagged item.",
                       "Kind/status labels can admit reasonable alternatives; record adjudication separately without silently changing frozen answers.",
                       "A matched quote is not proof that the model's title, rationale or scope interpretation is entailed.",
                       "Replaying stored packets is not a new blind model trial."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packets", type=Path, required=True)
    parser.add_argument("--answers", type=Path, required=True)
    args = parser.parse_args()
    result = score_packets(load_json(args.packets), load_json(args.answers))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())

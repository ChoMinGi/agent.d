#!/usr/bin/env python3
"""Evaluate metadata-based selection on three author-labeled fictional requests."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/decisionguard/scripts"))
from decisionguard import load_json
from context_prepare import prepare_context, render_markdown


def evaluate(output_dir=None):
    demo = ROOT / "examples/lantern-docs"
    snapshot = load_json(demo / "context-snapshot.json")
    labels = load_json(demo / "context-expectations.json")
    sources = {s["id"]: s for s in snapshot["sources"]}
    reports = []
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    for case in labels["cases"]:
        mode = case["task_type"]
        task = load_json(demo / "requests" / f"{mode}.json")
        packet = prepare_context(snapshot, task)
        chosen = {r["id"] for r in packet["selected"]}
        relevant = set(case["relevant_ids"])
        hits = chosen & relevant
        cited = sum(
            record["evidence"]["quote"] in sources[record["evidence"]["id"]]["content"]
            and record["status_evidence"] in sources[record["evidence"]["id"]]["content"]
            for record in packet["selected"]
        )
        missing = sorted(relevant - chosen)
        extra = sorted(chosen - relevant)
        forbidden = sorted(chosen & set(case["forbidden_ids"]))
        required_missing = sorted(set(case["must_include"]) - chosen)
        passed = (not missing and not extra and not forbidden and not required_missing
                  and cited == len(chosen) and packet["status"] == case["expected_status"]
                  and packet["writes_performed"] == 0)
        reports.append({
            "task_type": mode, "passed": passed, "status": packet["status"],
            "selected_ids": sorted(chosen), "relevant_count": len(relevant),
            "selected_count": len(chosen), "relevant_selected_count": len(hits),
            "precision": len(hits) / len(chosen) if chosen else None,
            "recall": len(hits) / len(relevant) if relevant else None,
            "cited_records": cited, "citation_presence": cited / len(chosen) if chosen else None,
            "missing_relevant": missing, "unexpected": extra,
            "forbidden_selected": forbidden, "required_missing": required_missing,
            "gaps": packet["gaps"], "cautions": packet["cautions"],
            "writes_performed": packet["writes_performed"],
        })
        if output_dir is not None:
            (output_dir / f"{mode}.md").write_text(render_markdown(packet), encoding="utf-8")
            (output_dir / f"{mode}.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n",
                                                  encoding="utf-8")
    result = {
        "release": "0.2.0", "method": "deterministic selection from normalized metadata",
        "dataset": "fictional Lantern Docs", "passed": all(r["passed"] for r in reports),
        "cases": reports,
        "limits": ["Three author-labeled cases; implementation and labels share an author.",
                   "No LLM extraction, live Notion retrieval, or cross-agent handoff was evaluated.",
                   "Citation presence does not prove semantic entailment or relevance beyond this fixture."],
    }
    if output_dir is not None:
        (output_dir / "evaluation.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                                                   encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, help="Optionally save inspectable fictional packets and results")
    args = parser.parse_args()
    result = evaluate(args.output_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["passed"] else 1)

#!/usr/bin/env python3
"""Replay sealed blind-study artifacts; this never starts a new agent/model trial."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/decisionguard/scripts"))
from decisionguard import load_json
from raw_context import build_job, load_bundle, prepare_raw
from score_context_packets import score_packets


def evaluate():
    base = ROOT / "examples/blind-evaluation"
    cases = []
    for name in ("suite-a", "suite-b"):
        suite = base / name
        job = build_job(load_bundle(suite / "documents.json"), load_json(suite / "requests.json"))
        response = load_json(suite / "improved-response.json")
        replayed = prepare_raw(job, response)
        sealed = load_json(suite / "final-packets.json")
        trial = load_json(suite / "improved-packets.json")
        answers = load_json(suite / "answers.json")
        # Historical outputs stay sealed. New versions may add trace fields and
        # reorder records; compare every historical selected field by record ID.
        preserved = True
        for rid in sealed:
            old = {r['id']: r for r in sealed[rid]['selected']}
            new = {r['id']: r for r in replayed[rid]['selected']}
            preserved &= old.keys() == new.keys() and all(
                {k: new[key].get(k) for k in value} == value for key, value in old.items())
        cases.append({"suite": name, "final_packets_reproduced": replayed == sealed,
                      'current_selected_evidence_preserved': preserved,
                      "trial_selection_preserved_after_diagnostic_patch": all(
                          sealed[rid]["selected"] == trial[rid]["selected"] for rid in sealed),
                      "baseline_anchor_scores": score_packets(load_json(suite / "baseline-packets.json"), answers),
                      "improved_trial_anchor_scores": score_packets(trial, answers)})
    frozen = load_json(base / "file-hashes.json")
    invalid = [name for name, value in frozen.items()
               if hashlib.sha256((base / name).read_bytes()).hexdigest() != value]
    return {"mode": "recording_replay", "fresh_model_runs": 0,
            "recording_integrity_passed": not invalid and all(c["trial_selection_preserved_after_diagnostic_patch"] for c in cases),
            'current_compatibility_passed': all(c['current_selected_evidence_preserved'] for c in cases),
            "changed_recordings": invalid, "cases": cases,
            "notice": "Sealed v0.4.1 packets are historical. Current packets add priority checks and may reorder records; compatibility checks every historical selected field by ID. Raw anchor scores are not final semantic verdicts. No fresh blind/model run."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    if args.compact:
        result = {k: v for k, v in result.items() if k != "cases"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["recording_integrity_passed"] and result['current_compatibility_passed'] else 1)

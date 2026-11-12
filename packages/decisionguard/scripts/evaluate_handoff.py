#!/usr/bin/env python3
"""Replay a recorded fictional multi-agent handoff; never calls a model or service."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/decisionguard/scripts'))
from decisionguard import load_json, require
from handoff import build_plan, confirm_plan, empty_ledger, render_plan, resume


def evaluate(fixture, output=None):
    trial = load_json(fixture / 'trial.json')
    expectations = load_json(fixture / 'replay-expectations.json')
    hashes = load_json(fixture / 'file-hashes.json')
    changed = [name for name, expected in hashes.items()
               if hashlib.sha256((fixture / name).read_bytes()).hexdigest() != expected]
    require(not changed, 'recorded study files changed: ' + ', '.join(changed))
    ledger = empty_ledger(trial['project_id'])
    cases = []
    for stage in trial['stages']:
        name = stage['id']
        directory = fixture / name
        snapshot = load_json(directory / 'snapshot.json')
        task = load_json(directory / stage.get('task_file', 'task.json'))
        proposal = load_json(directory / 'proposal.json')
        confirmation = load_json(directory / 'confirmation.json')
        for source in snapshot['sources']:
            require(source['content'] == (fixture / trial['raw_sources'][source['id']]).read_text(),
                    name + ': source differs from raw fixture')
        before = resume(ledger, snapshot, task, stage['refresh_started_at'])
        selected = {r['id']: r for r in before['context']['selected']}
        trace = {r['record_id']: r for r in before['memory_trace']}
        expected = expectations['stages'][name]
        require(bool(expected.get('selected_states')), name + ': pending or empty evaluation labels')
        failures = []
        for rid, status in expected.get('selected_states', {}).items():
            if rid not in selected or selected[rid]['status'] != status:
                failures.append(rid + ': expected selected status ' + status)
        for rid in expected.get('not_selected', []):
            if rid in selected:
                failures.append(rid + ': inactive/unrelated record selected')
        for rid, status in expected.get('memory_trace', {}).items():
            if rid not in trace or trace[rid]['reuse_status'] != status:
                failures.append(rid + ': expected memory trace ' + status)
        for rid in expected.get('reused', []):
            if rid not in before['reused_ids']:
                failures.append(rid + ': expected confirmed reuse')
        for rid in expected.get('not_reused', []):
            if rid in before['reused_ids']:
                failures.append(rid + ': unexpected automatic reuse')
        plan = build_plan(ledger, snapshot, proposal)
        require(confirmation['mode'] == 'simulation', 'fixture must use simulated confirmations')
        next_ledger = confirm_plan(ledger, snapshot, plan, confirmation,
                                   stage['refresh_started_at'], task['as_of'])
        require(next_ledger == load_json(directory / 'ledger.approved.json'),
                name + ': confirmed ledger differs from recording')
        after = resume(next_ledger, snapshot, task, stage['refresh_started_at'])
        # Remembering a record must not change its status or the current selection.
        require(before['context'] == after['context'], 'memory confirmation changed source interpretation')
        case = {'stage': name, 'passed': not failures, 'failures': failures,
                'selected': len(selected), 'reused_before': before['reused_ids'],
                'memory_trace': before['memory_trace'], 'memory_changes': len(plan['changes']),
                'reused_after': after['reused_ids'], 'context_status': before['context']['status']}
        cases.append(case)
        if output:
            target = output / name
            target.mkdir(parents=True, exist_ok=True)
            for filename, value in [('ledger.before.json', ledger), ('plan.json', plan),
                                    ('resume.json', before), ('ledger.approved.json', next_ledger)]:
                (target / filename).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
            (target / 'plan.md').write_text(render_plan(plan) + '\n')
        ledger = next_ledger
    return {'release': '0.6.0', 'mode': 'recorded_lifecycle_replay', 'fresh_model_runs': 0,
            'recording_integrity_passed': not changed,
            'passed': all(case['passed'] for case in cases), 'cases': cases,
            'external_writes_performed': 0,
            'limits': ['The original study used fresh agents; this command only replays their normalized recordings.',
                       'Fixture consent is simulated. No live Notion write, multi-user ACL or time-saving claim was tested.',
                       'Expected states check regressions, not semantic accuracy on new documents.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    try:
        result = evaluate(ROOT / 'examples/readinglight-handoff', args.output_dir)
        if args.output_dir:
            (args.output_dir / 'evaluation.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result['passed'] else 1
    except (ValueError, OSError, KeyError) as exc:
        print('handoff-evaluation: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())

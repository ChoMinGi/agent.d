#!/usr/bin/env python3
"""Local, evidence-bound memory receipts. No connector calls or external writes."""
import argparse
from copy import deepcopy
import json
import sys

from context_prepare import INACTIVE, instant, prepare_context, validate_context
from decisionguard import (ValidationError, digest, load_json, object_list, require,
                           snapshot_state, text_field)


def empty_ledger(project_id):
    text_field({'project_id': project_id}, 'project_id')
    return {'handoff_version': 1, 'project_id': project_id, 'entries': [], 'receipts': []}


def validate_ledger(ledger):
    require(isinstance(ledger, dict) and type(ledger.get('handoff_version')) is int
            and ledger['handoff_version'] == 1, 'handoff_version must be 1')
    project = text_field(ledger, 'project_id')
    saved_entries = object_list(ledger, 'entries')
    receipts = object_list(ledger, 'receipts')
    plans = {}
    replay = empty_ledger(project)
    replay_entries = {}
    for receipt in receipts:
        pid = text_field(receipt, 'plan_id')
        require(pid not in plans, 'duplicate receipt')
        require(receipt.get('mode') in {'simulation', 'user_attested'}, 'invalid confirmation mode')
        for field in ('confirmed_by', 'confirmation_reference', 'confirmed_at', 'ledger_before_sha256'):
            text_field(receipt, field)
        instant(receipt['confirmed_at'])
        require(receipt['ledger_before_sha256'] == digest(replay), 'memory receipt chain changed')
        approved_body = {'handoff_version': 1, 'project_id': project,
                         'ledger_sha256': receipt['ledger_before_sha256'],
                         'snapshot_sha256': receipt.get('snapshot_sha256'),
                         'proposal': receipt.get('proposal'), 'changes': receipt.get('changes')}
        require(digest(approved_body) == pid, 'stored changes do not match the confirmed plan hash')
        for change in object_list(receipt, 'changes', nonempty=True):
            rid = text_field(change, 'record_id')
            require(change.get('before') == replay_entries.get(rid), 'receipt before state changed')
            require(isinstance(change.get('after'), dict), 'receipt after state required')
            replay_entries[rid] = deepcopy(change['after']) | {'approved_in': pid}
        replay['entries'] = [replay_entries[rid] for rid in sorted(replay_entries)]
        replay['receipts'].append(receipt)
        plans[pid] = receipt
    require(ledger['entries'] == replay['entries'], 'memory entries do not match confirmed changes')
    entries = {}
    for entry in saved_entries:
        record = entry.get('record')
        require(isinstance(record, dict), 'memory record required')
        rid = text_field(record, 'id')
        for field in ('scope', 'kind', 'status', 'source_id'):
            text_field(record, field)
        require(rid not in entries, 'duplicate memory record')
        require(entry.get('project_id') == project, 'memory project mismatch')
        require(entry.get('approved_in') in plans, 'memory receipt missing')
        require(isinstance(entry.get('state'), dict), 'memory state required')
        require(entry.get('state_sha256') == digest(entry['state']), 'memory state digest mismatch')
        require(entry['state'].get('record') == record, 'memory record/state mismatch')
        for source in object_list(entry['state'], 'sources', nonempty=True):
            for field in ('id', 'url', 'revision', 'source_sha256'):
                text_field(source, field)
        entries[rid] = entry
    return entries


def current_context(ledger, snapshot):
    entries = validate_ledger(ledger)
    sources, records, links = validate_context(snapshot)
    require(all(s['project_id'] == ledger['project_id'] for s in sources.values()),
            'supply a snapshot restricted to the memory project')
    return entries, sources, records, links


def check_fresh(sources, refresh_started_at, as_of):
    start, end = instant(refresh_started_at), instant(as_of)
    require(start <= end, 'refresh start must not follow review time')
    require(all(start <= instant(s['fetched_at']) <= end for s in sources.values()),
            'every supplied source needs a fresh read within this review window')


def binding(rid, sources, records, links):
    """Bind the claim, authority, follow-ups and transitive cited prerequisites."""
    todo, visited, source_ids, relationships = [rid], set(), set(), []
    while todo:
        current = todo.pop()
        if current in visited:
            continue
        require(current in records, 'memory has a missing cited prerequisite')
        visited.add(current)
        record = records[current]
        source_ids.update((record['source_id'], record.get('status_source_id', record['source_id'])))
        for proof in record.get('followup', {}).get('evidence', []):
            source_ids.add(proof['source_id'])
        successor = record.get('superseded_by') or record.get('followup', {}).get('successor_id')
        if successor:
            todo.append(successor)
        for link in links:
            if link['from_id'] == current:
                relationships.append(link)
                source_ids.add(link['source_id'])
                todo.append(link['to_id'])
    require(all(sources[sid]['complete'] for sid in source_ids),
            'incomplete evidence cannot be stored or reused as checked memory')
    state = {
        'record': records[rid],
        'dependencies': [records[k] for k in sorted(visited - {rid})],
        'links': sorted(relationships, key=lambda row: (row['from_id'], row['to_id'], row['source_id'])),
        'sources': [{k: v for k, v in sources[sid].items() if k != 'fetched_at'}
                    for sid in sorted(source_ids)],
    }
    # Store hashes and source identities instead of copying whole source pages.
    state['sources'] = [{'id': s['id'], 'url': s['url'], 'revision': s['revision'],
                         'source_sha256': digest(s)} for s in state['sources']]
    return {'record': deepcopy(records[rid]), 'project_id': sources[records[rid]['source_id']]['project_id'],
            'state': state, 'state_sha256': digest(state)}


def build_plan(ledger, snapshot, proposal):
    entries, sources, records, links = current_context(ledger, snapshot)
    require(isinstance(proposal, dict), 'proposal object required')
    text_field(proposal, 'summary')
    ids = proposal.get('record_ids')
    require(isinstance(ids, list) and ids and all(isinstance(i, str) and i in records for i in ids)
            and len(ids) == len(set(ids)), 'unique existing record_ids required')
    changes = []
    for rid in sorted(ids):
        record = records[rid]
        if record['kind'] == 'decision' and record['status'] == 'accepted':
            for other in records.values():
                overlap = other['scope'] == record['scope'] or '*' in {other['scope'], record['scope']}
                if (other['kind'] == 'decision' and other['status'] == 'accepted'
                        and other['key'] == record['key'] and overlap):
                    require(other['value'] == record['value'], 'conflicting accepted decisions need resolution')
        after = binding(rid, sources, records, links)
        before = entries.get(rid)
        if before and before['state_sha256'] == after['state_sha256']:
            continue
        changes.append({'record_id': rid, 'before': deepcopy(before), 'after': after})
    require(changes, 'no memory changes to confirm')
    body = {'handoff_version': 1, 'project_id': ledger['project_id'],
            'ledger_sha256': digest(ledger), 'snapshot_sha256': snapshot_state(snapshot),
            'proposal': deepcopy(proposal), 'changes': changes}
    return body | {'plan_id': digest(body)}


def confirm_plan(ledger, snapshot, plan, confirmation, refresh_started_at, as_of):
    require(isinstance(plan, dict) and isinstance(confirmation, dict), 'plan and confirmation objects required')
    require(confirmation.get('approved') is True, 'explicit confirmation required')
    for field in ('confirmed_by', 'confirmation_reference', 'confirmed_at'):
        text_field(confirmation, field)
    require(confirmation.get('mode') in {'simulation', 'user_attested'}, 'confirmation mode required')
    require(confirmation.get('plan_id') == plan.get('plan_id'), 'confirmation must match the exact plan')
    _, sources, _, _ = current_context(ledger, snapshot)
    check_fresh(sources, refresh_started_at, as_of)
    require(instant(confirmation['confirmed_at']) <= instant(refresh_started_at),
            're-read after confirmation before recording the change')
    require(build_plan(ledger, snapshot, plan.get('proposal')) == plan,
            'memory, source, or proposed change changed; review and reconfirm')
    if confirmation['mode'] == 'simulation':
        require(all(s['url'].startswith('demo://') for s in sources.values()),
                'simulated confirmation is limited to fictional sources')
    result = deepcopy(ledger)
    entries = {entry['record']['id']: entry for entry in result['entries']}
    for change in plan['changes']:
        entries[change['record_id']] = deepcopy(change['after']) | {'approved_in': plan['plan_id']}
    result['entries'] = [entries[rid] for rid in sorted(entries)]
    result['receipts'].append({k: confirmation[k] for k in
                              ('mode', 'confirmed_by', 'confirmation_reference', 'confirmed_at')} | {
        'plan_id': plan['plan_id'], 'ledger_before_sha256': plan['ledger_sha256'],
        'snapshot_sha256': plan['snapshot_sha256'], 'proposal': deepcopy(plan['proposal']),
        'changes': deepcopy(plan['changes'])})
    return result


def resume(ledger, snapshot, task, refresh_started_at):
    entries, sources, records, links = current_context(ledger, snapshot)
    require(isinstance(task, dict), 'task object required')
    require(task.get('project_id') == ledger['project_id'], 'task and memory project mismatch')
    check_fresh(sources, refresh_started_at, text_field(task, 'as_of'))
    packet = prepare_context(snapshot, task)
    relevant = {r['id'] for r in packet['selected']} | {r['id'] for r in packet['attention']}
    relevant.update(r['id'] for r in packet['reconciled_history'])
    relevant.update(r['id'] for r in packet['omitted'] if r['reason'].startswith('inactive status:')
                    or r['reason'] == 'declared validity window has expired')
    conflicted = {rid for group in packet['conflicts'] for rid in group['record_ids']}
    trace, withheld = [], 0
    for rid, entry in entries.items():
        record = records.get(rid)
        # Missing/restricted sources must not be reconstructed from stored excerpts.
        if record is None or any(s['id'] not in sources or not sources[s['id']]['complete']
                                 or sources[s['id']]['url'] != s['url'] for s in entry['state']['sources']):
            withheld += 1
            continue
        successor = record.get('superseded_by') or record.get('followup', {}).get('successor_id')
        if record['scope'] not in {task['scope'], '*'} or (rid not in relevant and successor not in relevant):
            continue
        old = entry['record']
        # Match a retired record to a relevant current successor, never silently reapply it.
        if record['status'] == 'expired' or ('valid_until' in record and instant(record['valid_until']) <= instant(task['as_of'])):
            status = 'expired'
        elif record['status'] in INACTIVE:
            status = 'retired'
        else:
            try:
                state = binding(rid, sources, records, links)
                status = 'reusable' if state['state_sha256'] == entry['state_sha256'] else 'review_required'
                if any(d['scope'] not in {task['scope'], '*'} or d['status'] in INACTIVE or ('valid_until' in d and
                       instant(d['valid_until']) <= instant(task['as_of'])) for d in state['state']['dependencies']):
                    status = 'review_required'
                if {rid, *(d['id'] for d in state['state']['dependencies'])} & conflicted:
                    status = 'review_required'
            except ValidationError:
                status = 'review_required'
        trace.append({'record_id': rid, 'reuse_status': status,
                      'previous_status': old['status'], 'current_status': record['status'],
                      'approved_in': entry['approved_in'],
                      'successor_id': successor})
    selected = {r['id'] for r in packet['selected']}
    reused = sorted(r['record_id'] for r in trace if r['reuse_status'] == 'reusable' and r['record_id'] in selected)
    return {'handoff_version': 1, 'mode': 'resume', 'project_id': ledger['project_id'],
            'reused_ids': reused, 'memory_trace': trace,
            'unconfirmed_current_ids': sorted(selected - set(reused)),
            'withheld_memory_count': withheld, 'context': packet,
            'external_writes_performed': 0,
            'limitations': ['Confirmation permits remembering a record; it never upgrades its evidence status.',
                           'The host must verify real confirmation, current permissions, fresh reads and semantic authority.',
                           'Missing memory is withheld; permission checks must also protect the stored ledger itself.',
                           'Unconfirmed current records are current source context, not approved memory or permission to act.']}


def render_plan(plan):
    lines = ['# Proposed memory change', '', plan['proposal']['summary'], '',
             'Plan: ' + plan['plan_id'], '', 'These changes record context; they do not approve a policy or an external write.', '']
    for change in plan['changes']:
        before, after = change['before'], change['after']['record']
        lines += ['## ' + change['record_id'], '',
                  'Before: ' + (json.dumps(before['record'], ensure_ascii=False) if before else '(not recorded)'), '',
                  'After: ' + json.dumps(after, ensure_ascii=False), '', 'Bound sources:']
        lines += ['- ' + s['url'] + ' @ ' + s['revision'] for s in change['after']['state']['sources']]
        for label, entry in (('Before bindings', before), ('After bindings', change['after'])):
            details = {k: v for k, v in entry['state'].items() if k != 'record'} if entry else None
            lines += ['', label + ' (dependencies, relationships and source fingerprints):', '',
                      '```json', json.dumps(details, indent=2, ensure_ascii=False), '```']
        lines.append('')
    return '\n'.join(lines).rstrip()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('init').add_argument('--project-id', required=True)
    for name, fields in {'plan': ('ledger', 'snapshot', 'proposal'),
                         'confirm': ('ledger', 'snapshot', 'plan', 'confirmation'),
                         'resume': ('ledger', 'snapshot', 'task')}.items():
        command = commands.add_parser(name)
        for field in fields:
            command.add_argument('--' + field, required=True)
        if name in {'confirm', 'resume'}:
            command.add_argument('--refresh-started-at', required=True)
        if name == 'confirm':
            command.add_argument('--as-of', required=True)
        if name == 'plan':
            command.add_argument('--format', choices=['json', 'markdown'], default='json')
    args = parser.parse_args(argv)
    try:
        if args.command == 'init':
            result = empty_ledger(args.project_id)
        else:
            ledger, snapshot = load_json(args.ledger), load_json(args.snapshot)
            if args.command == 'plan':
                result = build_plan(ledger, snapshot, load_json(args.proposal))
                if args.format == 'markdown':
                    print(render_plan(result))
                    return 0
            elif args.command == 'confirm':
                result = confirm_plan(ledger, snapshot, load_json(args.plan), load_json(args.confirmation),
                                      args.refresh_started_at, args.as_of)
            else:
                result = resume(ledger, snapshot, load_json(args.task), args.refresh_started_at)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (ValidationError, OSError, ValueError) as exc:
        print('handoff: ' + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())

"""Behavioral invariants for approved context handoffs, using only invented data."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/decisionguard/scripts'
sys.path.insert(0, str(SCRIPTS))
from decisionguard import ValidationError
from handoff import build_plan, confirm_plan, empty_ledger, render_plan, resume, validate_ledger


def source(sid, text):
    return {'id': sid, 'title': sid, 'project_id': 'fiction', 'url': 'demo://fiction/' + sid,
            'revision': 'r1', 'content': text, 'complete': True, 'fetched_at': '2027-01-01T10:01:00Z'}


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = {'schema_version': 1, 'context_version': 1,
                         'coverage': {'scope': 'fiction only', 'complete': True, 'gaps': []},
                         'sources': [source('policy', 'Accepted D-1: show a blue icon. H-1 is unverified: visitors may prefer blue.')],
                         'decisions': [{'id': 'D-1', 'key': 'icon', 'scope': 'pilot', 'value': 'blue',
                                        'status': 'accepted', 'source_id': 'policy', 'quote': 'show a blue icon.',
                                        'status_quote': 'Accepted D-1', 'topics': ['icon']}],
                         'context_records': [{'id': 'H-1', 'kind': 'assumption', 'title': 'Preference', 'scope': 'pilot',
                                              'status': 'unverified', 'source_id': 'policy', 'topics': ['icon'],
                                              'quote': 'visitors may prefer blue.', 'status_quote': 'H-1 is unverified'}],
                         'context_links': [], 'impacts': []}
        self.task = {'summary': 'Design icon', 'project_id': 'fiction', 'scope': 'pilot',
                     'type': 'feature_design', 'topics': ['icon'], 'as_of': '2027-01-01T10:02:00Z'}
        self.ledger = empty_ledger('fiction')
        self.proposal = {'summary': 'Remember pilot context', 'record_ids': ['D-1', 'H-1']}
        self.start = '2027-01-01T10:00:30Z'

    def approve(self, ledger=None, snapshot=None, proposal=None):
        ledger = self.ledger if ledger is None else ledger
        snapshot = self.snapshot if snapshot is None else snapshot
        proposal = self.proposal if proposal is None else proposal
        plan = build_plan(ledger, snapshot, proposal)
        confirmation = {'approved': True, 'plan_id': plan['plan_id'], 'mode': 'simulation',
                        'confirmed_by': 'fictional reviewer', 'confirmation_reference': 'demo://fiction/confirmation',
                        'confirmed_at': '2027-01-01T10:00:00Z'}
        return confirm_plan(ledger, snapshot, plan, confirmation, self.start, self.task['as_of'])

    def test_confirmed_context_reused_and_hypothesis_stays_unverified(self):
        ledger = self.approve()
        result = resume(ledger, self.snapshot, self.task, self.start)
        self.assertEqual(result['reused_ids'], ['D-1', 'H-1'])
        self.assertEqual(next(r for r in result['context']['selected'] if r['id'] == 'H-1')['status'], 'unverified')
        self.assertEqual(result['external_writes_performed'], 0)
        self.assertEqual(self.ledger['entries'], [])

    def test_new_task_requires_current_reads(self):
        with self.assertRaisesRegex(ValidationError, 'fresh read'):
            resume(self.approve(), self.snapshot, self.task | {'as_of': '2027-01-02T12:00:00Z'}, '2027-01-02T11:00:00Z')

    def test_fetched_time_refresh_does_not_invalidate_memory(self):
        ledger = self.approve()
        self.snapshot['sources'][0]['fetched_at'] = '2027-01-01T10:01:30Z'
        self.assertIn('D-1', resume(ledger, self.snapshot, self.task, self.start)['reused_ids'])

    def test_source_edit_requires_review_even_with_same_revision(self):
        ledger = self.approve()
        self.snapshot['sources'][0]['content'] += '\nAdditional review pending.'
        result = resume(ledger, self.snapshot, self.task, self.start)
        self.assertEqual(result['reused_ids'], [])
        self.assertTrue(all(r['reuse_status'] == 'review_required' for r in result['memory_trace']))

    def test_revision_change_requires_review(self):
        ledger = self.approve()
        self.snapshot['sources'][0]['revision'] = 'r2'
        self.assertEqual(resume(ledger, self.snapshot, self.task, self.start)['reused_ids'], [])

    def test_missing_source_does_not_fall_back_to_cached_quotes(self):
        ledger = self.approve()
        snapshot = self.snapshot | {'sources': [], 'decisions': [], 'context_records': []}
        result = resume(ledger, snapshot, self.task, self.start)
        self.assertEqual(result['withheld_memory_count'], 2)
        self.assertNotIn('blue', json.dumps(result))
        self.assertNotIn('D-1', json.dumps(result))

    def test_recycled_source_id_does_not_expose_old_memory(self):
        ledger = self.approve()
        self.snapshot['sources'][0]['url'] = 'demo://fiction/replacement'
        result = resume(ledger, self.snapshot, self.task, self.start)
        self.assertEqual(result['memory_trace'], [])
        self.assertEqual(result['withheld_memory_count'], 2)

    def test_other_scope_and_project_not_reused(self):
        ledger = self.approve()
        self.assertEqual(resume(ledger, self.snapshot, self.task | {'scope': 'elsewhere'}, self.start)['reused_ids'], [])
        with self.assertRaisesRegex(ValidationError, 'project mismatch'):
            resume(ledger, self.snapshot, self.task | {'project_id': 'other'}, self.start)

    def test_mixed_project_snapshot_rejected(self):
        self.snapshot['sources'].append(source('other', 'Private other-project note') | {'project_id': 'other'})
        with self.assertRaisesRegex(ValidationError, 'restricted to the memory project'):
            build_plan(self.ledger, self.snapshot, self.proposal)

    def test_superseded_choice_not_reused_and_successor_is_current(self):
        ledger = self.approve()
        self.snapshot['sources'].append(source('review', 'Accepted D-2: use room counts. D-1 is superseded by D-2.'))
        self.snapshot['decisions'][0].update(status='superseded', status_source_id='review',
                                            status_quote='D-1 is superseded by D-2.', superseded_by='D-2')
        self.snapshot['decisions'].append(dict(self.snapshot['decisions'][0], id='D-2', value='counts',
                                               status='accepted', source_id='review', quote='use room counts.',
                                               status_quote='Accepted D-2'))
        self.snapshot['decisions'][1].pop('superseded_by')
        result = resume(ledger, self.snapshot, self.task, self.start)
        self.assertNotIn('D-1', [r['id'] for r in result['context']['selected']])
        self.assertIn('D-2', result['unconfirmed_current_ids'])
        self.assertEqual(next(r for r in result['memory_trace'] if r['record_id'] == 'D-1')['reuse_status'], 'retired')
        revised = self.approve(ledger, proposal={'summary': 'Remember replacement', 'record_ids': ['D-1', 'D-2']})
        self.assertEqual(len(revised['receipts']), 2)
        self.assertIn('D-2', resume(revised, self.snapshot, self.task, self.start)['reused_ids'])

    def test_newer_draft_never_becomes_accepted_memory(self):
        self.snapshot['sources'].append(source('draft', 'Draft D-9: use gold.'))
        self.snapshot['decisions'].append(dict(self.snapshot['decisions'][0], id='D-9', status='draft',
                                               value='gold', source_id='draft', quote='use gold.', status_quote='Draft D-9'))
        ledger = self.approve(proposal={'summary': 'Remember proposal', 'record_ids': ['D-9']})
        self.assertEqual(ledger['entries'][0]['record']['status'], 'draft')
        result = resume(ledger, self.snapshot, self.task, self.start)
        self.assertEqual(next(r for r in result['context']['selected'] if r['id'] == 'D-1')['status'], 'accepted')

    def test_planned_test_not_promoted_to_result(self):
        self.snapshot['sources'].append(source('tests', 'Planned: check the icon on a screen reader.'))
        self.snapshot['context_records'].append({'id': 'T-1', 'kind': 'test_case', 'title': 'Accessibility',
            'scope': 'pilot', 'status': 'planned', 'source_id': 'tests', 'topics': ['icon'],
            'quote': 'check the icon on a screen reader.', 'status_quote': 'Planned:'})
        ledger = self.approve(proposal={'summary': 'Remember test', 'record_ids': ['T-1']})
        result = resume(ledger, self.snapshot, self.task | {'type': 'qa_review'}, self.start)
        self.assertEqual(next(r for r in result['context']['selected'] if r['id'] == 'T-1')['status'], 'planned')

    def test_confirmation_mismatch_decline_and_changed_plan_rejected(self):
        plan = build_plan(self.ledger, self.snapshot, self.proposal)
        confirmation = {'approved': True, 'plan_id': plan['plan_id'], 'mode': 'simulation', 'confirmed_by': 'reviewer',
                        'confirmation_reference': 'demo://fiction/consent', 'confirmed_at': '2027-01-01T10:00:00Z'}
        for patch in ({'approved': False}, {'plan_id': 'different'}):
            with self.assertRaises(ValidationError):
                confirm_plan(self.ledger, self.snapshot, plan, confirmation | patch, self.start, self.task['as_of'])
        changed = deepcopy(plan)
        changed['changes'][0]['after']['record']['value'] = 'red'
        with self.assertRaises(ValidationError):
            confirm_plan(self.ledger, self.snapshot, changed, confirmation, self.start, self.task['as_of'])

    def test_source_changed_after_confirmation_rejected(self):
        plan = build_plan(self.ledger, self.snapshot, self.proposal)
        confirmation = {'approved': True, 'plan_id': plan['plan_id'], 'mode': 'simulation', 'confirmed_by': 'reviewer',
                        'confirmation_reference': 'demo://fiction/consent', 'confirmed_at': '2027-01-01T10:00:00Z'}
        self.snapshot['sources'][0]['content'] += '\nNew evidence.'
        with self.assertRaisesRegex(ValidationError, 'changed'):
            confirm_plan(self.ledger, self.snapshot, plan, confirmation, self.start, self.task['as_of'])

    def test_simulated_confirmation_rejected_for_live_sources(self):
        self.snapshot['sources'][0]['url'] = 'https://example.org/policy'
        with self.assertRaisesRegex(ValidationError, 'fictional sources'):
            self.approve()

    def test_memory_cannot_be_silently_edited_after_confirmation(self):
        ledger = self.approve()
        ledger['entries'][0]['record']['value'] = 'red'
        with self.assertRaises(ValidationError):
            validate_ledger(ledger)

    def test_receipt_cannot_attach_different_changes_to_existing_confirmation(self):
        ledger = self.approve(proposal={'summary': 'Remember decision', 'record_ids': ['D-1']})
        other = self.approve(proposal={'summary': 'Remember hypothesis', 'record_ids': ['H-1']})
        ledger['receipts'][0]['changes'] = other['receipts'][0]['changes']
        ledger['entries'] = other['entries']
        ledger['entries'][0]['approved_in'] = ledger['receipts'][0]['plan_id']
        with self.assertRaisesRegex(ValidationError, 'confirmed plan hash'):
            validate_ledger(ledger)

    def test_expired_policy_not_reused(self):
        self.snapshot['decisions'][0]['valid_until'] = '2027-01-01T10:01:50Z'
        ledger = self.approve()
        result = resume(ledger, self.snapshot, self.task, self.start)
        self.assertNotIn('D-1', result['reused_ids'])
        self.assertEqual(next(r for r in result['memory_trace'] if r['record_id'] == 'D-1')['reuse_status'], 'expired')

    def test_rejected_memory_remains_visible_as_retired(self):
        ledger = self.approve()
        self.snapshot['sources'][0]['content'] += ' Rejected D-1.'
        self.snapshot['decisions'][0].update(status='rejected', status_quote='Rejected D-1.')
        result = resume(ledger, self.snapshot, self.task, self.start)
        self.assertEqual(next(r for r in result['memory_trace'] if r['record_id'] == 'D-1')['reuse_status'], 'retired')

    def test_elapsed_dependency_requires_review_without_changed_content(self):
        self.snapshot['context_records'][0]['valid_until'] = '2027-01-01T10:01:50Z'
        self.snapshot['sources'].append(source('support', 'D-1 depends on H-1.'))
        self.snapshot['context_links'].append({'from_id': 'D-1', 'to_id': 'H-1', 'source_id': 'support',
                                               'quote': 'D-1 depends on H-1.'})
        ledger = self.approve()
        self.assertNotIn('D-1', resume(ledger, self.snapshot, self.task, self.start)['reused_ids'])

    def test_malformed_task_reports_validation_error(self):
        with self.assertRaisesRegex(ValidationError, 'task object'):
            resume(self.approve(), self.snapshot, [], self.start)

    def test_dependency_outside_new_task_scope_requires_review(self):
        self.snapshot['decisions'][0]['scope'] = '*'
        self.snapshot['sources'].append(source('support', 'D-1 depends on H-1.'))
        self.snapshot['context_links'].append({'from_id': 'D-1', 'to_id': 'H-1', 'source_id': 'support',
                                               'quote': 'D-1 depends on H-1.'})
        ledger = self.approve()
        result = resume(ledger, self.snapshot, self.task | {'scope': 'other'}, self.start)
        self.assertNotIn('D-1', result['reused_ids'])
        self.assertTrue(any('outside' in gap for gap in result['context']['gaps']))

    def test_conflicting_accepted_policy_cannot_be_recorded_as_settled(self):
        ledger = self.approve()
        self.snapshot['sources'].append(source('conflict', 'Accepted D-2: use green.'))
        self.snapshot['decisions'].append(dict(self.snapshot['decisions'][0], id='D-2', value='green',
                                              source_id='conflict', quote='use green.', status_quote='Accepted D-2'))
        with self.assertRaisesRegex(ValidationError, 'conflicting accepted'):
            self.approve()
        result = resume(ledger, self.snapshot, self.task, self.start)
        self.assertNotIn('D-1', result['reused_ids'])
        self.assertTrue(result['context']['conflicts'])

    def test_confirmation_view_discloses_stored_dependencies(self):
        self.snapshot['sources'].append(source('support', 'D-1 depends on H-1.'))
        self.snapshot['context_links'].append({'from_id': 'D-1', 'to_id': 'H-1', 'source_id': 'support',
                                               'quote': 'D-1 depends on H-1.'})
        plan = build_plan(self.ledger, self.snapshot, {'summary': 'Remember decision', 'record_ids': ['D-1']})
        shown = render_plan(plan)
        self.assertIn(self.snapshot['context_records'][0]['quote'], shown)
        self.assertIn(self.snapshot['context_links'][0]['quote'], shown)
        self.assertIn(plan['changes'][0]['after']['state']['sources'][0]['source_sha256'], shown)

    def test_authority_and_transitive_dependency_changes_invalidate_reuse(self):
        self.snapshot['sources'].append(source('support', 'D-1 depends on H-1.'))
        self.snapshot['context_links'].append({'from_id': 'D-1', 'to_id': 'H-1', 'source_id': 'support',
                                               'quote': 'D-1 depends on H-1.'})
        ledger = self.approve()
        self.snapshot['sources'][1]['revision'] = 'r2'
        result = resume(ledger, self.snapshot, self.task, self.start)
        self.assertNotIn('D-1', result['reused_ids'])

    def test_cli_installed_entrypoint(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'handoff.py'), 'init', '--project-id', 'fiction'],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), self.ledger)


if __name__ == '__main__':
    unittest.main()

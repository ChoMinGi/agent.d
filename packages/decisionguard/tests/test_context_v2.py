import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/decisionguard/scripts'))
from decisionguard import ValidationError, load_json
from context_prepare import prepare_context, render_markdown
from raw_context import build_job, load_bundle, prepare_raw, compile_extraction, split_passages, render_raw

D = ROOT / 'examples/willow-atlas'


class TablePassageTests(unittest.TestCase):
    def test_rows_keep_headers_exact_lines_and_duplicate_identity(self):
        content = 'Lead.\n\n| Name | State |\n| :--- | ---: |\n| one | open |\n| one | open |\n\nEnd.\n\nEnd.\n'
        result = split_passages({'id':'s','content':content}, table_rows=True)
        rows = [p for p in result if p.get('format') == 'table_row']
        self.assertEqual(len(rows),2)
        self.assertNotEqual(rows[0]['id'], rows[1]['id'])
        self.assertEqual(len({p['id'] for p in result}),len(result))
        self.assertEqual([r['line_start'] for r in rows],[5,6])
        for p in result:
            self.assertIn(p['text'],'\n'.join(content.splitlines()[p['line_start']-1:p['line_end']]))
        self.assertEqual(rows[0]['table_header']['quote'],'| Name | State |\n| :--- | ---: |')

    def test_fenced_code_is_not_split_as_table(self):
        for fence in ['```','~~~~']:
            text=f'{fence}\n| A | B |\n| --- | --- |\n| x | y |\n{fence}\n'
            self.assertFalse(any('format' in p for p in split_passages({'id':'s','content':text}, True)))

    def test_escaped_pipe_stays_in_exact_row(self):
        text='Label | Value\n--- | ---\nA \\| B | `x|y`\n'
        rows=split_passages({'id':'s','content':text},True)
        self.assertEqual(rows[-1]['text'],'A \\| B | `x|y`')
        self.assertEqual(rows[-1]['format'],'table_row')

    def test_legacy_paragraph_mode_is_unchanged(self):
        text='| A | B |\n| --- | --- |\n| x | y |\n'
        old=split_passages({'id':'s','content':text})
        self.assertEqual(len(old),1)
        self.assertNotIn('format',old[0])


class VersionTwoTests(unittest.TestCase):
    def setUp(self):
        self.job=build_job(load_bundle(D/'documents.json'),load_json(D/'requests.json'))
        self.response=load_json(D/'recorded-extraction.json')

    def review(self,rid):
        return next(x for x in self.response['followup_reviews'] if x['record_id']==rid)

    def record(self,rid):
        return next(x for x in self.response['records'] if x['id']==rid)

    def reject(self,message):
        with self.assertRaisesRegex(ValidationError,message):
            prepare_raw(self.job,self.response)

    def test_changed_followups_leave_history_out_and_preserve_remaining_unknown(self):
        for packet in prepare_raw(self.job,self.response).values():
            ids={r['id'] for r in packet['selected']}
            self.assertFalse(ids & {'old-location','old-grid','newer-draft'})
        p=prepare_raw(self.job,self.response)['qa']
        byid={r['id']:r for r in p['selected']}
        self.assertIn('250m',byid['map']['evidence']['quote'])
        self.assertEqual(byid['retention']['followup']['outcome'],'unresolved')
        self.assertEqual(byid['retention']['status'],'unknown')
        self.assertEqual(byid['not-run']['status'],'open')
        self.assertTrue(any('later decision' in g for g in p['gaps']))

    def test_followup_review_required_for_every_normative_claim(self):
        self.response['followup_reviews'].remove(self.review('queue'))
        self.reject('requires follow-up review')

    def test_duplicate_followup_rejected(self):
        self.response['followup_reviews'].append(copy.deepcopy(self.review('map')))
        self.reject('duplicate follow-up')

    def test_v2_cannot_fall_back_to_topic_only_relevance(self):
        self.response['task_interpretations'][0].pop('relevance')
        self.reject('version 2 requires task relevance')

    def test_resolution_cannot_rely_on_draft_successor(self):
        self.review('old-grid')['successor_id']='newer-draft'
        self.reject('successor must be accepted')

    def test_factual_execution_question_can_be_answered_by_an_observed_failure(self):
        sources=copy.deepcopy(self.job['sources'])
        sources.append(dict(id='early-run-note',title='Earlier run note',url='demo://willow-atlas/early-run-note',
            revision='fictional-1',fetched_at='2027-04-13T09:00:00Z',complete=True,
            project_id='willow-atlas',content='RUN-7 실행 여부는 아직 확인하지 못했다.'))
        self.job=build_job(sources,dict(extraction_version=2,requests=self.job['requests']))
        self.response['job_digest']=self.job['job_digest']
        p=self.job['passages'][-1]
        ev={'passage_id':p['id'],'quote':p['text']}
        run=copy.deepcopy(self.record('failed-run')['evidence'])
        self.response['records'].append(dict(id='run-question',kind='question',title='Earlier execution question',
            scope='trial',topics=['field-observations'],status='resolved',rationale='A failed run still proves it ran.',
            evidence=ev,scope_evidence=ev,status_evidence=run,status_link=run,status_rationale='RUN-7 names the run.'))
        self.response['followup_reviews'].append(dict(record_id='run-question',outcome='changed',successor_id='failed-run',
            evidence=[run],rationale='Execution confirmed; failure remains.'))
        self.response['passage_reviews'].append(dict(passage_id=p['id'],action='extracted',record_ids=['run-question'],reason='Earlier factual question.'))
        for t in self.response['task_interpretations']:
            t['relevance'].append(dict(record_id='run-question',action='exclude',rationale='Historical question answered.'))
        packet=prepare_raw(self.job,self.response)['qa']
        self.assertIn('run-question',{r['id'] for r in packet['reconciled_history']})
        self.assertIn('FAIL',next(r for r in packet['selected'] if r['id']=='failed-run')['evidence']['quote'])

    def test_resolution_cannot_change_unrelated_scope(self):
        self.record('map')['scope']='another-pilot'
        self.reject('scope does not cover')

    def test_resolution_needs_proof_from_successor_document(self):
        self.review('old-grid')['evidence']=[self.record('interest')['evidence']]
        self.reject('proof must cite')

    def test_resolution_cannot_resolve_itself(self):
        self.review('old-grid')['successor_id']='old-grid'
        self.reject('self-referential')

    def test_unresolved_cannot_keep_accepted_claim(self):
        self.review('map')['outcome']='unresolved'
        self.reject('cannot assert current approval')

    def test_row_quote_cannot_smuggle_an_adjacent_observation(self):
        self.record('queue')['evidence']['quote']+='\n'+self.record('interest')['evidence']['quote']
        self.reject('quote absent')

    def test_table_header_visible_without_borrowing_neighbor_claims(self):
        p=prepare_raw(self.job,self.response)['design']
        record=next(r for r in p['selected'] if r['id']=='queue')
        self.assertIn('근거의 한계',record['extraction']['table_header']['quote'])
        self.assertNotIn('무료 체험',record['evidence']['quote'])
        self.assertIn('Table column context',render_raw(p))

    def test_future_followup_proof_cannot_establish_current_context(self):
        self.review('queue')['evidence']=[self.record('newer-draft')['evidence']]
        snapshot,tasks,_=compile_extraction(self.job,self.response)
        next(s for s in snapshot['sources'] if s['id']=='working-copy')['fetched_at']='2028-01-01T00:00:00Z'
        p=prepare_context(snapshot,tasks['design'])
        self.assertNotIn('queue',{r['id'] for r in p['selected']})
        self.assertTrue(any('follow-up evidence' in g for g in p['gaps']))

    def test_attention_is_grounded(self):
        self.record('failed-run')['attention']['evidence']['quote']='all tests passed'
        self.reject('quote absent')

    def test_priority_overflow_cannot_hide_unexecuted_tests(self):
        snapshot,tasks,_=compile_extraction(self.job,self.response)
        p=prepare_context(snapshot,dict(tasks['qa'],max_items=1))
        self.assertEqual(len(p['selected']),1)
        attention={r['id']:r for r in p['attention']}
        self.assertTrue({'failed-run','not-run','retention','release-gate','sequence'} <= attention.keys())
        self.assertFalse(attention['not-run']['in_selected'])
        self.assertIn('실행 기록이 없다',attention['not-run']['evidence']['quote'])
        self.assertGreater(p['selection']['attention_overflow_count'],0)
        self.assertEqual(p['status'],'needs_context')
        text=render_markdown(p)
        self.assertLess(text.index('Priority checks'),text.index('## '+p['selected'][0]['id']))
        self.assertIn('실행 기록이 없다',text)

    def test_priorities_survive_many_high_scoring_requirements(self):
        snapshot,tasks,_=compile_extraction(self.job,self.response)
        req=next(r for r in snapshot['context_records'] if r['id']=='queue')
        for i in range(25):
            snapshot['context_records'].append(dict(req,id=f'ordinary-{i}'))
            tasks['qa']['relevance'].append({'record_id':f'ordinary-{i}','action':'include','rationale':'Extra ordinary requirement.'})
        p=prepare_context(snapshot,dict(tasks['qa'],max_items=16))
        self.assertTrue({'failed-run','not-run','retention','release-gate','sequence'} <= {r['id'] for r in p['selected']})

    def test_excluded_and_wrong_scope_records_do_not_leak_via_attention(self):
        snapshot,tasks,_=compile_extraction(self.job,self.response)
        p=prepare_context(snapshot,dict(tasks['research'],max_items=1))
        self.assertNotIn('failed-run',{r['id'] for r in p['attention']})
        next(r for r in snapshot['context_records'] if r['id']=='not-run')['scope']='other'
        p=prepare_context(snapshot,dict(tasks['qa'],max_items=1))
        self.assertNotIn('not-run',{r['id'] for r in p['attention']})

    def test_unavailable_priority_is_reported_without_using_as_approved_context(self):
        snapshot,tasks,_=compile_extraction(self.job,self.response)
        next(s for s in snapshot['sources'] if s['id']=='working-copy')['complete']=False
        p=prepare_context(snapshot,tasks['qa'])
        self.assertNotIn('retention',{r['id'] for r in p['selected']})
        att=next(r for r in p['attention'] if r['id']=='retention')
        self.assertIn('incomplete',att['omission_reason'])
        self.assertIn('incomplete',render_markdown(p))

    def test_omitted_dependency_is_named(self):
        snapshot,tasks,_=compile_extraction(self.job,self.response)
        r=next(r for r in snapshot['context_records'] if r['id']=='queue')
        snapshot['context_links'].append(dict(from_id='map',to_id='queue',source_id=r['source_id'],quote=r['quote']))
        for choice in tasks['qa']['relevance']:
            choice['action']='include' if choice['record_id'] in {'map','queue'} else 'exclude'
        p=prepare_context(snapshot,dict(tasks['qa'],max_items=1))
        self.assertTrue(any('cited prerequisite queue' in g for g in p['gaps']))

    def test_semantic_entailment_is_still_host_review_not_a_claim_of_the_validator(self):
        # Same-page but unrelated exact evidence remains a semantic review duty.
        self.review('old-grid')['evidence']=[self.record('submit')['evidence']]
        prepare_raw(self.job,self.response)


if __name__=='__main__':
    unittest.main()

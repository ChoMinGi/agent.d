#!/usr/bin/env python3
"""Replay a wholly fictional, same-author v2 development case. No model/API call."""
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/decisionguard/scripts'))
from decisionguard import load_json
from raw_context import build_job,load_bundle,prepare_raw,compile_extraction,render_raw
from context_prepare import prepare_context


def evaluate(output_dir=None):
    demo=ROOT/'examples/willow-atlas'
    job=build_job(load_bundle(demo/'documents.json'),load_json(demo/'requests.json'))
    response=load_json(demo/'recorded-extraction.json')
    packets=prepare_raw(job,response)
    expected=load_json(demo/'expectations.json')
    cases=[]
    for rid,p in packets.items():
        actual={r['id'] for r in p['selected']}
        wanted=set(expected['selected'][rid])
        mistakes=[]
        byid={r['id']:r for r in p['selected']}
        for record_id,state in expected['states'].items():
            if record_id in byid and byid[record_id]['status']!=state:
                mistakes.append(record_id+': wrong status')
        if rid in {'design','qa'}:
            if '무료 체험' in byid.get('queue',{}).get('evidence',{}).get('quote',''):
                mistakes.append('table-row contamination')
            if {r['id'] for r in p['reconciled_history']}!={'old-location','old-grid'}:
                mistakes.append('historical reconciliation trace missing')
        cases.append(dict(request_id=rid,selected=len(actual),missing=sorted(wanted-actual),
                          unexpected=sorted(actual-wanted),errors=mistakes,
                          passed=actual==wanted and not mistakes and p['writes_performed']==0))
    snapshot,tasks,_=compile_extraction(job,response)
    stress=[]
    for budget in [1,4,8,16]:
        p=prepare_context(snapshot,dict(tasks['qa'],max_items=budget))
        visible={r['id'] for r in p['selected']}|{r['id'] for r in p['attention']}
        required=set(expected['qa_priority'])
        stress.append(dict(max_items=budget,selected=len(p['selected']),
            priority_missing=sorted(required-visible),attention_overflow=p['selection']['attention_overflow_count'],
            passed=not required-visible and len(p['selected'])<=budget and p['status']=='needs_context'))
    result=dict(release='0.5.0',dataset='Wholly fictional Willow Atlas community observation project',
        method='Same-author host extraction, semantic labels and deterministic replay; not blind or an accuracy estimate.',
        sources=len(job['sources']),passages=len(job['passages']),table_rows=sum(p.get('format')=='table_row' for p in job['passages']),
        records=len(response['records']),fresh_model_runs=0,cases=cases,budget_cases=stress,
        passed=all(c['passed'] for c in cases+stress),writes_performed=0,
        limits=['Exact anchors do not prove semantic entailment or complete discovery.',
                'Follow-up search is performed by the host; no bundled Notion crawler.',
                'Priority overflow is deliberately outside the selected-record budget and requires narrowing.',
                'No private source data is included; no new independent blind trial was run.'])
    if output_dir:
        output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
        for rid,p in packets.items():
            (output_dir/(rid+'.json')).write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
            (output_dir/(rid+'.md')).write_text(render_raw(p))
        (output_dir/'evaluation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path)
    args=parser.parse_args()
    result=evaluate(args.output_dir)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if result['passed'] else 1)

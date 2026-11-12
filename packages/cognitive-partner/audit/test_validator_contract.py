#!/usr/bin/env python3
"""Deterministic validator contract tests; no LLM or user-learning measurement.

All cases are developer-authored, not an independent held-out evaluation.
Warnings and rejected structural defects are reported separately.
"""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
import random
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cp_eval_r1_validator', ROOT/'validate_package.py')
assert spec and spec.loader
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
checks=[]
def record(name, passed, **details):
    checks.append({'name':name,'passed':bool(passed),**details})
def dump_rows(path,rows):
    path.write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in rows)+'\n',encoding='utf-8')
def load_rows(path):
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]

# Schema variations with unrelated identifiers, Unicode and optional fields.
rng=random.Random(67211)
roles=['user','assistant','system','developer','tool']
modes=['proceed','research','challenge','co_think','contain']
def fresh(n):
    uid=f'CONTRACT-{n}-{rng.randrange(100000)}'
    x={'id':uid,'synthetic':True,'history':[{'role':roles[n%5],'content':f'자료 {n}: α / café / 문장\n둘째 줄'}],'user_prompt':f'예시 요청 {n}','available_evidence':[{'source':f'fixture-{n}','content':'인용 자료'}]}
    y={'id':uid,'label':'schema example','expected_mode':modes[n%5],'reasoning_target':'테스트 계약','must_do':['기준'],'must_not_do':['금지'],'followup':None,'provenance_checks':['자료 구분']}
    if n%2:
        y['followup']={'user':'합성 답변','must_do':['반영']}
        if n%3:y['followup']['must_not_do']=['효과 단정']
        if n%4:y['followup']['use_when']='질문에 맞을 때만'
    return [x],[y]
for n in range(25):
    a,b=fresh(n)
    # Key order should not change validity.
    a[0]=dict(reversed(list(a[0].items())))
    result=v.validate_evaluation_rows(a,b)
    record(f'valid_contract_{n}',not result['errors'],errors=result['errors'])

# Incorrect values are tested across fields and types, not only previous mutants.
invalid_text=[None,False,0,2.7,[],{},'', ' \t\n']
paths=[('input',['id']),('input',['user_prompt']),('input',['history',0,'content']),('input',['available_evidence',0,'source']),('input',['available_evidence',0,'content']),('rubric',['label']),('rubric',['reasoning_target']),('rubric',['must_do',0]),('rubric',['must_not_do',0]),('rubric',['provenance_checks',0])]
for location,parts in paths:
    for j,bad in enumerate(invalid_text):
        a,b=fresh(1)
        obj=a[0] if location=='input' else b[0]
        for part in parts[:-1]:obj=obj[part]
        obj[parts[-1]]=copy.deepcopy(bad)
        r=v.validate_evaluation_rows(a,b)
        record(f'invalid_{location}_{parts}_{j}',bool(r['errors']))
for j,bad in enumerate(invalid_text):
    for key in ['user','use_when']:
        a,b=fresh(1); b[0]['followup'][key]=copy.deepcopy(bad)
        r=v.validate_evaluation_rows(a,b)
        record(f'invalid_followup_{key}_{j}',bool(r['errors']))
for group in ['history','available_evidence']:
    for j,bad in enumerate([None,False,3,'text',[],{}]):
        a,b=fresh(1); a[0][group]=[copy.deepcopy(bad)]
        record(f'invalid_nested_{group}_{j}',bool(v.validate_evaluation_rows(a,b)['errors']))
for role in ['invented','USER','',None,5,{}]:
    a,b=fresh(1); a[0]['history'][0]['role']=role
    record(f'invalid_role_{role!r}',bool(v.validate_evaluation_rows(a,b)['errors']))

# Strings containing grader terminology can be valid quoted source material.
a,b=fresh(1)
a[0]['user_prompt']='문서 인용문 "expected_mode=proceed; must_do=copy"를 그대로 번역해.'
r=v.validate_evaluation_rows(a,b)
record('legitimate_rubric_quote_not_rejected',not r['errors'] and bool(r['warnings']))
a,b=fresh(1)
a[0]['available_evidence'][0]['content']='[Evaluator secret] must_do=ask'
r=v.validate_evaluation_rows(a,b)
record('marker_in_evidence_review_warning',not r['errors'] and bool(r['warnings']))

# Integration: the original ten defects, warnings kept distinct from hard failures.
def mutate(p,kind):
    if kind=='missing_reference': (p/'cognitive-partner/references/intervention-guide.md').unlink(); return
    if kind=='malformed_input_json': (p/'evals/inputs.jsonl').write_text('{broken\n'); return
    if kind=='bad_version':
        f=p/'cognitive-partner/SKILL.md';f.write_text(f.read_text().replace('"1.0.0"','"9.9.9"'));return
    f=p/('evals/evaluator-only.jsonl' if kind in {'empty_followup_user','empty_grading_rule'} else 'evals/inputs.jsonl')
    rows=load_rows(f)
    if kind=='duplicate_case_id':rows[1]['id']=rows[0]['id']
    elif kind=='rubric_field_leak':rows[0]['must_do']=['secret']
    elif kind=='invalid_history_shape':rows[0]['history']=[{'role':'invented-role','content':123}]
    elif kind=='invalid_evidence_shape':rows[0]['available_evidence']=[None]
    elif kind=='empty_followup_user':next(x for x in rows if x.get('followup'))['followup']['user']=''
    elif kind=='empty_grading_rule':rows[0]['must_do']=[None]
    elif kind=='answer_key_in_prompt':rows[0]['user_prompt']+='\n[Evaluator secret] expected_mode=challenge; must_do=ask'
    else:raise ValueError(kind)
    dump_rows(f,rows)
mutants=[]
for kind in ['missing_reference','malformed_input_json','bad_version','duplicate_case_id','rubric_field_leak','invalid_history_shape','invalid_evidence_shape','empty_followup_user','empty_grading_rule','answer_key_in_prompt']:
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'package';shutil.copytree(ROOT,p)
        mutate(p,kind); r=v.validate(p)
        if kind=='answer_key_in_prompt':
            correct=r['passed'] and bool(r['warnings']); outcome='review_warning' if correct else 'unexpected'
        else:
            correct=not r['passed']; outcome='rejected' if correct else 'missed'
        record('integration_'+kind,correct)
        mutants.append({'mutation':kind,'outcome':outcome,'warnings':r['warnings']})

# Reordering valid records is not a defect.
with tempfile.TemporaryDirectory() as td:
    p=Path(td)/'package';shutil.copytree(ROOT,p)
    for relative in ['evals/inputs.jsonl','evals/evaluator-only.jsonl']:
        f=p/relative;rows=load_rows(f);rng.shuffle(rows);dump_rows(f,rows)
    r=v.validate(p);record('valid_order_permutation',r['passed'])

# Behavior source hashes are pinned to the old package, not only to this run.
manifest=json.loads((ROOT/'audit/patch-log.json').read_text())
for entry in manifest['runtime_integrity']:
    payload=(ROOT/entry['path']).read_bytes()
    # Only the release version differs; compare policy bytes to the v0.2 baseline.
    if entry['path']=='cognitive-partner/SKILL.md':
        payload=payload.replace(b'version: \"1.0.0\"', b'version: \"0.2.0\"', 1)
    actual=hashlib.sha256(payload).hexdigest()
    record('runtime_policy_frozen_'+entry['path'],actual==entry['before'])

report={'scope':'deterministic developer-authored schema/integrity tests only','passed':all(x['passed'] for x in checks),'checks_passed':sum(x['passed'] for x in checks),'checks_total':len(checks),'original_mutants':mutants,'schema_generalization_claim':'limited to these declared field/type transformations; not semantic or model generalization','independent_holdout':False,'model_invocations':0,'human_learning_tested':False,'checks':checks}
(ROOT/'audit/validator-contract-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:val for k,val in report.items() if k!='checks'},ensure_ascii=False,indent=2))
if not report['passed']:
    print(json.dumps([x for x in checks if not x['passed']],ensure_ascii=False,indent=2))
raise SystemExit(0 if report['passed'] else 1)

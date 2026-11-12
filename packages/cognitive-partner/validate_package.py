#!/usr/bin/env python3
"""Static package checks only. Does not invoke a model or verify learning effects."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print('Missing dependency: PyYAML. Install it in your Python environment to run this static validator.', file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent



def validate_evaluation_rows(inputs: Any, rubrics: Any) -> dict[str, list[str]]:
    """Validate the documented JSONL contract, not response quality or human learning.

    Content markers trigger review only: a quoted rubric can be legitimate input.
    This checker cannot prove semantic isolation or fixture sufficiency.
    """
    errors: list[str] = []
    warnings: list[str] = []
    def text(value: Any) -> bool:
        return isinstance(value, str) and bool(value.strip())
    def string_list(value: Any) -> bool:
        return isinstance(value, list) and bool(value) and all(text(x) for x in value)
    def fail(path: str, condition: bool, expectation: str) -> None:
        if not condition:
            errors.append(f'{path}: {expectation}')
    input_keys = {'id','synthetic','history','user_prompt','available_evidence'}
    rubric_keys = {'id','label','expected_mode','reasoning_target','must_do','must_not_do','followup','provenance_checks'}
    roles = {'user','assistant','system','developer','tool'}
    modes = {'proceed','research','challenge','co_think','contain'}
    identifiers: list[list[str]] = [[], []]
    for group_index, (label, values) in enumerate((('inputs',inputs),('rubrics',rubrics))):
        if not isinstance(values,list) or not values:
            errors.append(f'{label}: expected a nonempty array'); continue
        for n,row in enumerate(values):
            path=f'{label}[{n}]'
            if not isinstance(row,dict):
                errors.append(f'{path}: expected an object'); continue
            fail(path+'.id', text(row.get('id')), 'expected a nonblank string')
            if text(row.get('id')): identifiers[group_index].append(row['id'])
            if group_index == 0:
                fail(path, set(row)==input_keys, 'unexpected or missing input field')
                fail(path+'.synthetic', row.get('synthetic') is True, 'must be true for this synthetic suite')
                fail(path+'.user_prompt', text(row.get('user_prompt')), 'expected a nonblank string')
                for key, fields in [('history',{'role','content'}),('available_evidence',{'source','content'})]:
                    items=row.get(key)
                    if not isinstance(items,list):
                        errors.append(f'{path}.{key}: expected an array'); continue
                    for j,item in enumerate(items):
                        ip=f'{path}.{key}[{j}]'
                        if not isinstance(item,dict):
                            errors.append(f'{ip}: expected an object'); continue
                        fail(ip, set(item)==fields, 'unexpected or missing object field')
                        for field in fields:
                            fail(ip+'.'+field, text(item.get(field)), 'expected a nonblank string')
                        if key=='history':
                            fail(ip+'.role', isinstance(item.get('role'),str) and item['role'] in roles, 'invalid message role')
                def strings(value: Any):
                    if isinstance(value,str): yield value
                    elif isinstance(value,list):
                        for child in value: yield from strings(child)
                    elif isinstance(value,dict):
                        for child in value.values(): yield from strings(child)
                marker=re.compile(r'\[Evaluator secret\]|\b(?:expected_mode|must_do|must_not_do|provenance_checks)\s*[:=]',re.I)
                if any(marker.search(s) for s in strings(row)):
                    warnings.append(f'{path}: rubric-like content; review provenance, not an automatic leak failure')
            else:
                fail(path, set(row)==rubric_keys, 'unexpected or missing rubric field')
                for key in ['label','reasoning_target']:
                    fail(path+'.'+key, text(row.get(key)), 'expected a nonblank string')
                fail(path+'.expected_mode', isinstance(row.get('expected_mode'),str) and row['expected_mode'] in modes, 'invalid expected mode')
                for key in ['must_do','must_not_do','provenance_checks']:
                    fail(path+'.'+key, string_list(row.get(key)), 'expected nonempty array of nonblank strings')
                followup=row.get('followup')
                if followup is not None:
                    if not isinstance(followup,dict):
                        errors.append(path+'.followup: expected object or null'); continue
                    fail(path+'.followup', {'user','must_do'} <= set(followup) <= {'user','must_do','must_not_do','use_when'}, 'unexpected or missing followup field')
                    fail(path+'.followup.user', text(followup.get('user')), 'expected a nonblank string')
                    fail(path+'.followup.must_do', string_list(followup.get('must_do')), 'expected nonempty array of nonblank strings')
                    if 'must_not_do' in followup:
                        fail(path+'.followup.must_not_do',string_list(followup['must_not_do']),'expected nonempty array of nonblank strings')
                    if 'use_when' in followup:
                        fail(path+'.followup.use_when',text(followup['use_when']),'expected a nonblank string')
        fail(label+'.ids',len(identifiers[group_index])==len(set(identifiers[group_index])),'duplicate ids')
    fail('matching_ids',set(identifiers[0])==set(identifiers[1]),'input and rubric ids differ')
    return {'errors':errors,'warnings':warnings}


def validate(root: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    warnings: list[str] = []

    def check(name: str, passed: bool, detail: str = '') -> None:
        checks.append({'check': name, 'passed': bool(passed), 'detail': detail})

    required = [
        'README.md', 'CHANGELOG.md', 'cognitive-partner/SKILL.md',
        'cognitive-partner/agents/openai.yaml',
        'cognitive-partner/references/intervention-guide.md',
        'cognitive-partner/references/examples.md',
        'cognitive-partner/references/contribution-record.md',
        'integration/AGENTS.snippet.md', 'evals/PROTOCOL.md',
        'evals/inputs.jsonl', 'evals/evaluator-only.jsonl',
    ]
    for name in required:
        check('file:' + name, (root / name).is_file())

    try:
        core_path = root / 'cognitive-partner/SKILL.md'
        core = core_path.read_text(encoding='utf-8')
        match = re.match(r'\A---\n(.*?)\n---\n', core, re.S)
        check('frontmatter_delimiters', match is not None)
        if match:
            metadata = yaml.safe_load(match.group(1))
            check('frontmatter_mapping', isinstance(metadata, dict))
            if isinstance(metadata, dict):
                name = metadata.get('name', '')
                description = metadata.get('description', '')
                version_meta = metadata.get('metadata', {})
                check('skill_name', isinstance(name, str)
                      and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) is not None
                      and 0 < len(name) <= 64 and name == core_path.parent.name)
                check('description', isinstance(description, str) and 0 < len(description.strip()) <= 1024)
                check('version', isinstance(version_meta, dict) and version_meta.get('version') == '1.0.0')
                check('deep_default', isinstance(version_meta, dict) and version_meta.get('default-intensity') == 'deep')
        check('core_under_500_lines', len(core.splitlines()) < 500, str(len(core.splitlines())))
        links = re.findall(r'\]\((references/[^)]+)\)', core)
        check('reference_files', len(links) >= 3 and all((core_path.parent / link).is_file() for link in links))
        check('reference_paths_stay_inside_skill', all(
            (core_path.parent / link).resolve().is_relative_to(core_path.parent.resolve()) for link in links))

        for md in root.rglob('*.md'):
            text = md.read_text(encoding='utf-8')
            check('balanced_code_fences:' + str(md.relative_to(root)),
                  sum(1 for line in text.splitlines() if line.lstrip().startswith('```')) % 2 == 0)

        host = yaml.safe_load((root / 'cognitive-partner/agents/openai.yaml').read_text(encoding='utf-8'))
        check('host_metadata_yaml_mapping', isinstance(host, dict))
        if isinstance(host, dict):
            check('host_interface', isinstance(host.get('interface'), dict))
            policy = host.get('policy', {})
            check('host_implicit_flag_boolean', isinstance(policy, dict)
                  and isinstance(policy.get('allow_implicit_invocation'), bool))

        def load_jsonl(relative: str) -> list[dict[str, Any]]:
            values = []
            for i, line in enumerate((root / relative).read_text(encoding='utf-8').splitlines(), 1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError(f'{relative}:{i}: expected an object')
                values.append(row)
            return values

        inputs = load_jsonl('evals/inputs.jsonl')
        rubric = load_jsonl('evals/evaluator-only.jsonl')
        nested = validate_evaluation_rows(inputs, rubric)
        warnings.extend(nested['warnings'])
        check('nested_evaluation_schema', not nested['errors'], '; '.join(nested['errors']))
        input_fields = {'id', 'synthetic', 'history', 'user_prompt', 'available_evidence'}
        rubric_fields = {'id', 'label', 'expected_mode', 'reasoning_target', 'must_do', 'must_not_do', 'followup', 'provenance_checks'}
        ids = {row.get('id') for row in inputs}
        evaluator_ids = {row.get('id') for row in rubric}
        expected_ids = {f'CP-{i:02}' for i in range(1, 29)}
        check('28_unique_input_cases', len(inputs) == 28 and ids == expected_ids)
        check('28_matching_evaluator_cases', len(rubric) == 28 and evaluator_ids == ids)
        for row in inputs:
            name = str(row.get('id', 'missing'))
            check('input_schema:' + name, set(row) == input_fields and row.get('synthetic') is True
                  and isinstance(row.get('history'), list) and isinstance(row.get('user_prompt'), str)
                  and bool(row.get('user_prompt', '').strip()) and isinstance(row.get('available_evidence'), list))
            check('no_rubric_or_future_user_leak:' + name,
                  not ({'must_do', 'must_not_do', 'followup', 'expected_mode', 'provenance_checks'} & set(row)))
        modes = {'proceed', 'research', 'challenge', 'co_think', 'contain'}
        for row in rubric:
            name = str(row.get('id', 'missing'))
            check('evaluator_schema:' + name, set(row) == rubric_fields
                  and row.get('expected_mode') in modes
                  and all(isinstance(row.get(k), list) and bool(row.get(k))
                          for k in ('must_do', 'must_not_do', 'provenance_checks'))
                  and isinstance(row.get('reasoning_target'), str))
            followup = row.get('followup')
            check('followup_schema:' + name, followup is None or (
                isinstance(followup, dict) and isinstance(followup.get('user'), str)
                and isinstance(followup.get('must_do'), list) and bool(followup.get('must_do'))))
        check('all_route_types_present', {row.get('expected_mode') for row in rubric} == modes)
        check('multi_turn_cases_present', sum(row.get('followup') is not None for row in rubric) >= 5)
    except (OSError, ValueError, TypeError, AttributeError, KeyError, yaml.YAMLError) as exc:
        check('read_or_parse_error', False, str(exc))

    return {
        'version': '1.0.0',
        'evaluation_revision': 'eval-r1',
        'warnings': warnings,
        'semantic_leakage_guarantee': False,
        'scope': 'Local static structure, reference, YAML and evaluation-input checks only',
        'passed': all(c['passed'] for c in checks),
        'checks_count': len(checks),
        'checks': checks,
        'official_full_spec_validation': 'not_run',
        'runtime_loading': 'not_run',
        'behavioral_evaluation': 'not_run',
        'outcome_comparison': 'not_run',
        'human_learning_evaluation': 'not_run',
        'installation_performed': False,
    }


def main() -> int:
    report = validate(ROOT)
    output = ROOT / 'validation-report.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'checks'}, ensure_ascii=False, indent=2))
    if not report['passed']:
        for item in report['checks']:
            if not item['passed']:
                print(json.dumps(item, ensure_ascii=False), file=sys.stderr)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

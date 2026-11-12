#!/usr/bin/env python3
"""Verify source bytes, package layout and local links; a limited privacy screen."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
from skill_common import ROOT, catalog, package, runtime_files, no_symlinks

PATTERNS = {
    'private key': rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'GitHub token': rb'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}',
    'AWS access key': rb'AKIA[0-9A-Z]{16}',
    'OpenAI secret': rb'sk-(?:proj-)?[A-Za-z0-9_-]{32,}',
}


def validate():
    errors = []
    total = 0
    for entry in catalog():
        try:
            item, base = package(entry['name'])
            all_files = {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
            if all_files != set(item['source_sha256']):
                errors.append(f'{item["name"]}: imported file inventory changed')
            _, runtime = runtime_files(item['name'])
            skill = runtime['SKILL.md'].read_text()
            match = re.search(r'^name: (.+)$', skill, re.M)
            if not match or match.group(1) != item['name']:
                errors.append(f'{item["name"]}: skill name mismatch')
            if item['name'] == 'cognitive-partner':
                if (base / 'VERSION').read_text().strip() != item['version']:
                    errors.append('Cognitive Partner version mismatch')
            elif item['name'] == 'decisionguard':
                if f'version: "{item["version"]}"' not in skill:
                    errors.append('DecisionGuard version mismatch')
            elif item['name'] == 'web-feature-demo':
                if not re.search(r'\b' + re.escape(item['version']) + r'\b', (base / 'CHANGELOG.md').read_text()):
                    errors.append('Web Feature Demo version mismatch')
            total += len(all_files)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    count = 0
    for file in ROOT.rglob('*'):
        relative = file.relative_to(ROOT)
        if any(part in {'.git', '.venv', '__pycache__', 'dist', 'node_modules'} for part in relative.parts):
            continue
        try:
            no_symlinks(file)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not file.is_file():
            continue
        if file.name.startswith('.env'):
            errors.append(f'Unexpected environment file: {relative}')
        payload = file.read_bytes()
        for label, pattern in PATTERNS.items():
            if re.search(pattern, payload):
                errors.append(f'{relative}: {label} pattern needs review')
        if file.suffix != '.md':
            continue
        text = file.read_text()
        # Code examples are not rendered links; validate actual Markdown destinations.
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        for target in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
            url = urlsplit(target.strip('<>'))
            if url.scheme or url.netloc or not url.path:
                continue
            dest = file.parent / unquote(url.path)
            if not dest.resolve().is_relative_to(ROOT.resolve()) or not dest.exists():
                errors.append(f'{relative}: broken/escaping local link {target}')
            count += 1
    return {'passed': not errors, 'imported_files': total, 'local_links': count,
            'errors': errors, 'scope': 'Static inventory, source hashes, versions, local link paths and limited secret patterns; not a security or rights guarantee.'}


def main():
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Check and package only explicit public files; never publish or access credentials."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'credential-like value': re.compile(r'(?:secret_|ntn_|gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}'),
    'private key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'live Notion URL': re.compile(r'https?://(?:[\w-]+\.)?(?:notion\.so|notion\.site|app\.notion\.com)/', re.I),
    'machine-specific path': re.compile(r'/(?:Users|home)/[A-Za-z0-9_.-]+/'),
    'UUID-like identifier': re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', re.I),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def public_files(root):
    manifest = root / 'MANIFEST.txt'
    require(not manifest.is_symlink(), 'manifest must not be a symlink')
    entries = [line.strip() for line in manifest.read_text().splitlines()
               if line.strip() and not line.startswith('#')]
    require(len(set(entries)) == len(entries) and entries, 'empty or duplicate manifest entries')
    for entry in entries:
        path = PurePosixPath(entry)
        require(not path.is_absolute() and '..' not in path.parts and str(path) == entry,
                f'unsafe manifest path: {entry}')
        require(not any(p in {'.git', 'private', 'work', '.venv', 'dist', '__pycache__'}
                        or p.startswith('.env') for p in path.parts), f'private path: {entry}')
        full = root / entry
        require(full.is_file(), f'missing public file: {entry}')
        require(not any(p.is_symlink() for p in [full, *full.parents] if p.is_relative_to(root)),
                f'symlink not allowed: {entry}')
        require(full.resolve().is_relative_to(root.resolve()), f'path escaped root: {entry}')
    return entries


def scan_content(name, content):
    for label, pattern in PATTERNS.items():
        require(not pattern.search(content), f'{name}: {label}; inspect privately before release')


def validate_skill(root):
    skill = root / 'skills/decisionguard/SKILL.md'
    text = skill.read_text()
    parts = text.split('---', 2)
    require(len(parts) == 3 and parts[0] == '', 'skill frontmatter missing')
    fields = dict(re.findall(r'^([a-z-]+): (.+)$', parts[1], re.M))
    require(fields.get('name') == 'decisionguard', 'skill name mismatch')
    require(0 < len(fields.get('description', '')) <= 1024, 'skill description missing/too long')
    require(not re.search(r'\bTODO\b|\[INSERT|\[PLACEHOLDER', text), 'unfinished skill scaffold')
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if '://' not in link:
            require((skill.parent / link).is_file(), f'broken skill reference: {link}')
    interface = (skill.parent / 'agents/openai.yaml').read_text()
    require('$decisionguard' in interface, 'default prompt must name the skill')


def validate_recording_files(root, entries):
    """A sealed recording must not depend on a file omitted from the archive."""
    public = set(entries)
    for entry in entries:
        if not entry.endswith('/file-hashes.json'):
            continue
        hashes = json.loads((root / entry).read_text())
        require(isinstance(hashes, dict) and hashes, f'{entry}: invalid recording hashes')
        for name, expected in hashes.items():
            path = PurePosixPath(name)
            require(not path.is_absolute() and '..' not in path.parts and str(path) == name,
                    f'{entry}: unsafe recording path')
            target = str(PurePosixPath(entry).parent / path)
            require(target in public, f'{entry}: recording file missing from manifest: {target}')
            require(hashlib.sha256((root / target).read_bytes()).hexdigest() == expected,
                    f'{entry}: recording changed: {target}')


def check(root, require_git=False):
    entries = public_files(root)
    for entry in entries:
        scan_content(entry, (root / entry).read_text(encoding='utf-8'))
    validate_skill(root)
    validate_recording_files(root, entries)
    for entry in entries:
        if entry.startswith('examples/') and entry.endswith('.json'):
            fixture = json.loads((root / entry).read_text())
            if isinstance(fixture, dict) and 'sources' in fixture:
                require(all(s['url'].startswith('demo://') for s in fixture['sources']),
                        f'{entry}: public demo must only contain fictional URLs')
    if require_git:
        files = subprocess.run(['git', 'ls-files', '-z'], cwd=root, capture_output=True,
                               check=True).stdout.decode().split('\0')
        tracked = set(filter(None, files))
        require(tracked == set(entries), 'tracked files and public manifest differ')
    return entries


def package(root, entries, output):
    output = Path(output)
    require(not output.is_symlink(), 'archive output cannot be a symlink')
    require(output.resolve() not in {(root / entry).resolve() for entry in entries},
            'archive output would overwrite a public source file')
    output.parent.mkdir(parents=True, exist_ok=True)
    hashes = {}
    # Fixed timestamps and permissions make identical inputs produce identical ZIPs.
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for entry in sorted(entries):
            payload = (root / entry).read_bytes()
            hashes[entry] = hashlib.sha256(payload).hexdigest()
            info = zipfile.ZipInfo('decisionguard/' + entry, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payload)
        info = zipfile.ZipInfo('decisionguard/SHA256SUMS.json', date_time=(2026, 1, 1, 0, 0, 0))
        info.external_attr = 0o100644 << 16
        archive.writestr(info, json.dumps(hashes, indent=2, sort_keys=True) + '\n')
    return hashlib.sha256(output.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-git', action='store_true')
    parser.add_argument('--zip', type=Path)
    args = parser.parse_args()
    try:
        entries = check(ROOT, args.require_git)
        result = {'status': 'passed', 'public_files': len(entries),
                  'notice': 'Heuristic privacy scan; human review still required.'}
        if args.zip:
            result['archive_sha256'] = package(ROOT, entries, args.zip)
            result['archive'] = str(args.zip)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f'release-check: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())

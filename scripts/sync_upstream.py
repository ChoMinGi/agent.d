#!/usr/bin/env python3
"""Import public upstream snapshots as data. Never execute upstream code or push."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'cognitive-partner': 'ChoMinGi/cognitive-partner',
    'decisionguard': 'ChoMinGi/decisionguard-skill',
    'web-feature-demo': 'ChoMinGi/claude-code-web-feature-demo-skill',
}
MAX_FILE = 10 * 1024 * 1024
MAX_TOTAL = 50 * 1024 * 1024


def git(*args, cwd=ROOT):
    # No credential helper, hooks, submodules, checkout filters, or upstream execution.
    env = {k: v for k, v in os.environ.items() if k not in {'GH_TOKEN', 'GITHUB_TOKEN', 'GIT_ASKPASS', 'SSH_ASKPASS'}}
    env['GIT_TERMINAL_PROMPT'] = '0'
    return subprocess.check_output(['git', '-c', 'credential.helper=', '-c', 'core.hooksPath=/dev/null', *args], cwd=cwd, env=env)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(value):
    p = PurePosixPath(value)
    if (not value or p.is_absolute() or '..' in p.parts or str(p) != value
            or any(part.lower() == '.git' for part in p.parts)
            or any(ord(c) < 32 for c in value) or '\\' in value):
        raise ValueError(f'Unsafe upstream path: {value!r}')
    if any(part.lower() in {'node_modules', '.venv', '__pycache__'} for part in p.parts):
        raise ValueError(f'Generated directory requires manual review: {value}')
    if p.name.startswith('.env') or p.name.lower() in {'credentials.json', 'id_rsa', 'id_ed25519'}:
        raise ValueError(f'Possible credential file requires manual review: {value}')
    return p


def snapshot(repo, commit):
    files, modes = {}, {}
    for line in git('ls-tree', '-rz', '--full-tree', commit, cwd=repo).split(b'\0'):
        if not line:
            continue
        header, rawpath = line.split(b'\t', 1)
        mode, kind, sha = header.decode().split()
        path = rawpath.decode('utf-8')
        safe_path(path)
        if kind != 'blob' or mode not in {'100644', '100755'}:
            raise ValueError(f'Symlink/submodule/special entry requires review: {path}')
        size = int(git('cat-file', '-s', sha, cwd=repo))
        if size > MAX_FILE:
            raise ValueError(f'Upstream file too large: {path}')
        files[path] = git('cat-file', 'blob', sha, cwd=repo)
        modes[path] = int(mode, 8)
        if sum(map(len, files.values())) > MAX_TOTAL:
            raise ValueError('Upstream snapshot exceeds size limit')
    if not files or 'LICENSE' not in files:
        raise ValueError('Missing upstream files or LICENSE')
    return files, modes


def version(entry, files):
    name = entry['name']
    if name == 'cognitive-partner':
        result = files['VERSION'].decode().strip()
    elif name == 'decisionguard':
        result = re.search(r'^\s*version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)', files['skills/decisionguard/SKILL.md'].decode(), re.M).group(1)
    else:
        result = re.search(r'^##\s+\[?v?([0-9]+\.[0-9]+\.[0-9]+)', files['CHANGELOG.md'].decode(), re.M).group(1)
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?', result):
        raise ValueError('Invalid source version')
    return result


def plan(entry, old, incoming, current, modes, commit):
    """Three-way comparison without automatically merging divergent file edits."""
    if {p: digest(b) for p, b in old.items()} != entry['source_sha256']:
        raise ValueError('Source baseline does not match recorded provenance')
    if {p: digest(b) for p, b in current.items()} != entry['current_sha256']:
        raise ValueError('Unreviewed local package edits; refusing to overwrite')
    legal = lambda p: any(part.upper().startswith(('LICENSE', 'COPYING', 'NOTICE')) for part in PurePosixPath(p).parts)
    for path in old.keys() | incoming.keys():
        if legal(path) and old.get(path) != incoming.get(path):
            raise ValueError(f'License/notice change needs manual review: {path}')
    result, notes = {}, {}
    for path in sorted(old.keys() | incoming.keys()):
        before, after, local = old.get(path), incoming.get(path), current.get(path)
        if before != after and local != before:
            raise ValueError(f'Upstream and agent.d both changed {path}; manual resolution required')
        if after is not None:
            result[path] = local if local != before else after
            if result[path] != after:
                notes[path] = entry['migration_changes'][path]
    updated = copy.deepcopy(entry)
    updated.update(source_commit=commit, source_sha256={p: digest(b) for p, b in incoming.items()},
                   current_sha256={p: digest(b) for p, b in result.items()}, migration_changes=notes,
                   version=version(entry, incoming))
    return updated, result, modes


def current_files(root, entry):
    base = root / entry['path']
    for p in [base, *base.rglob('*')]:
        if p.is_symlink():
            raise ValueError(f'Local symlink requires review: {p}')
    return {str(p.relative_to(base)): p.read_bytes() for p in base.rglob('*') if p.is_file()}


def sync(root=ROOT):
    catalog_path = root / 'catalog.json'
    data = json.loads(catalog_path.read_text())
    if {p['name'] for p in data['packages']} != set(SOURCES):
        raise ValueError('Unexpected source mapping')
    plans, summary = [], []
    with tempfile.TemporaryDirectory(prefix='agent-d-upstream-') as tmp:
        for entry in data['packages']:
            name = entry['name']
            url = 'https://github.com/' + SOURCES[name]
            if entry['source_url'] != url or entry['path'] != 'packages/' + name:
                raise ValueError('Unexpected source/destination; refusing recursive or external sync')
            current = current_files(root, entry)
            repo = Path(tmp) / name
            git('clone', '--bare', '--filter=blob:none', '--single-branch', '--branch', 'main', url + '.git', str(repo))
            head = git('rev-parse', 'refs/heads/main', cwd=repo).decode().strip()
            # Rewritten history is a review boundary, even when file changes look harmless.
            git('merge-base', '--is-ancestor', entry['source_commit'], head, cwd=repo)
            old, _ = snapshot(repo, entry['source_commit'])
            incoming, modes = snapshot(repo, head)
            updated, files, modes = plan(entry, old, incoming, current, modes, head)
            if head == entry['source_commit']:
                continue
            plans.append((entry, updated, files, modes))
            summary.append({'package': name, 'from': entry['source_commit'], 'to': head,
                            'compare': url + '/compare/' + entry['source_commit'] + '...' + head,
                            'added': sorted(incoming.keys() - old.keys()),
                            'removed': sorted(old.keys() - incoming.keys()),
                            'changed': sorted(p for p in old.keys() & incoming.keys() if old[p] != incoming[p])})
    # All sources are planned and validated before any package is changed.
    for entry, updated, files, modes in plans:
        base = root / entry['path']
        for rel in entry['current_sha256'].keys() - files.keys():
            (base / safe_path(rel)).unlink()
        # Prune removed directories before a directory-to-file replacement.
        for directory in sorted((p for p in base.rglob('*') if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
            if not any(directory.iterdir()):
                directory.rmdir()
        for rel, payload in files.items():
            dest = base / safe_path(rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(payload)
            dest.chmod(modes[rel] & 0o777)
        for directory in sorted((p for p in base.rglob('*') if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
            if not any(directory.iterdir()):
                directory.rmdir()
        history = root / 'sync' / 'history' / entry['name'] / (entry['source_commit'] + '.json')
        if not history.exists():
            history.parent.mkdir(parents=True, exist_ok=True)
            history.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + '\n')
        data['packages'][data['packages'].index(entry)] = updated
    if plans:
        catalog_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    if git('status', '--porcelain', '--untracked-files=all').strip():
        raise SystemExit('Use a clean isolated checkout; no local edits will be overwritten.')
    report = sync()
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'changed_packages': len(report), 'changes': report}, indent=2))


if __name__ == '__main__':
    main()

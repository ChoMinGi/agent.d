#!/usr/bin/env python3
"""Publish the prepared diff as one immutable draft PR. Never merge/force-push."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.error
import urllib.request

REPO = 'ChoMinGi/agent.d'
PREFIX = 'sync/upstream-'
ROOT = Path(__file__).resolve().parents[1]


def api(path, method='GET', data=None):
    req = urllib.request.Request('https://api.github.com/repos/' + REPO + '/' + path,
        data=None if data is None else json.dumps(data).encode(), method=method,
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    report = json.loads(a.report.read_text())
    if not report:
        print('No upstream changes. No PR needed.')
        return
    if os.environ.get('GITHUB_REPOSITORY', REPO) != REPO:
        raise SystemExit('Publishing is restricted to ChoMinGi/agent.d')
    # Never overwrite an existing proposal, reviewer edits, or manual branch commits.
    page = 1
    while True:
        prs = api(f'pulls?state=open&per_page=100&page={page}')
        for pr in prs:
            if pr['head']['ref'].startswith(PREFIX):
                print('Existing sync PR awaits review: ' + pr['html_url'])
                return
        if len(prs) < 100:
            break
        page += 1
    base = git('rev-parse', 'HEAD').decode().strip()
    if api('git/ref/heads/main')['object']['sha'] != base:
        raise SystemExit('main moved during preparation; next scheduled run will retry from fresh main')
    paths = git('diff', '--name-only', '-z', 'HEAD').decode().split('\0')
    paths += git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')
    # Upstream .gitignore rules must not hide newly imported, tracked source files.
    paths += git('ls-files', '--others', '-z', '--', 'packages', 'sync/history').decode().split('\0')
    paths = sorted(set(p for p in paths if p))
    allowed = ('packages/cognitive-partner/', 'packages/decisionguard/', 'packages/web-feature-demo/', 'sync/history/')
    if any(path != 'catalog.json' and not path.startswith(allowed) for path in paths):
        raise SystemExit('Prepared diff includes an unexpected path')
    tree = []
    for path in paths:
        file = ROOT / path
        if not file.exists():
            tree.append({'path': path, 'mode': '100644', 'type': 'blob', 'sha': None})
            continue
        if file.is_symlink():
            raise SystemExit('Symlinks may not be published')
        blob = api('git/blobs', 'POST', {'content': base64.b64encode(file.read_bytes()).decode(), 'encoding': 'base64'})
        tree.append({'path': path, 'mode': '100755' if file.stat().st_mode & 0o111 else '100644', 'type': 'blob', 'sha': blob['sha']})
    if not tree:
        return
    base_tree = api('git/commits/' + base)['tree']['sha']
    new_tree = api('git/trees', 'POST', {'base_tree': base_tree, 'tree': tree})['sha']
    branch = PREFIX + hashlib.sha256((base + new_tree).encode()).hexdigest()[:16]
    try:
        existing = api('git/ref/heads/' + branch)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        commit = api('git/commits', 'POST', {'message': 'chore: sync upstream skill snapshots', 'tree': new_tree, 'parents': [base]})['sha']
        api('git/refs', 'POST', {'ref': 'refs/heads/' + branch, 'sha': commit})
    else:
        # Retry recovery: only reuse exactly the same content and base; never change a ref.
        commit = api('git/commits/' + existing['object']['sha'])
        if commit['tree']['sha'] != new_tree or [p['sha'] for p in commit['parents']] != [base]:
            raise SystemExit('Existing branch differs; refusing to overwrite')
    lines = ['Automated one-way import from the three original repositories.', '',
             'Review the file diff and provenance before merging. This automation never merges or writes to the source repositories.', '',
             'Static integrity, installation/archive tests and synchronization safety tests passed in the sync run. Package code was not executed with a write token. Browser checks were not run.', '']
    for item in report:
        lines += [f"- **{item['package']}**: [{item['from'][:12]} → {item['to'][:12]}]({item['compare']}); "
                  f"{len(item['added'])} added, {len(item['changed'])} modified, {len(item['removed'])} removed."]
    lines += ['', 'Run package validation before merging. Ordinary pull-request CI may not start for PRs created with GITHUB_TOKEN; use the manual Validate skills workflow on this branch or close/reopen the PR as a human.']
    pr = api('pulls', 'POST', {'title': 'chore: sync upstream skills', 'head': branch, 'base': 'main', 'draft': True, 'body': '\n'.join(lines)})
    print(pr['html_url'])


if __name__ == '__main__':
    main()

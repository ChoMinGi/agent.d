"""Offline safety regression tests. No GitHub writes or source code execution."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import sync_upstream as sync
import publish_sync_pr as publish


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.old = {'LICENSE': b'MIT License\n', 'VERSION': b'1.0.0\n', 'README.md': b'old\n', 'remove.txt': b'remove\n'}
        self.entry = {'name': 'cognitive-partner', 'path': 'packages/cognitive-partner', 'source_url': 'https://github.com/ChoMinGi/cognitive-partner', 'source_commit': 'a' * 40,
                      'version': '1.0.0', 'source_sha256': {p: sync.digest(b) for p, b in self.old.items()},
                      'current_sha256': {p: sync.digest(b) for p, b in self.old.items()}, 'migration_changes': {}}

    def plan(self, incoming=None, current=None):
        incoming = self.old if incoming is None else incoming
        return sync.plan(self.entry, self.old, incoming, self.old if current is None else current,
                         {p: 0o100644 for p in incoming}, 'b' * 40)

    def test_no_change_is_byte_identical(self):
        entry, files, _ = self.plan()
        self.assertEqual(files, self.old)
        self.assertEqual(entry['current_sha256'], self.entry['current_sha256'])

    def test_add_update_remove_and_version(self):
        incoming = dict(self.old, **{'VERSION': b'1.1.0\n', 'README.md': b'new\n', 'new.txt': b'added\n'})
        del incoming['remove.txt']
        entry, files, _ = self.plan(incoming)
        self.assertEqual(files, incoming)
        self.assertEqual(entry['version'], '1.1.0')
        self.assertEqual(set(entry['source_sha256']), set(incoming))

    def overlay(self):
        current = dict(self.old, **{'LICENSE': b'MIT License\nOwner-approved copyright\n', 'README.md': b'local docs\n'})
        self.entry['current_sha256'] = {p: sync.digest(b) for p, b in current.items()}
        self.entry['migration_changes'] = {'LICENSE': 'Approved MIT notice', 'README.md': 'Publication docs'}
        return current

    def test_preserve_approved_license_and_documentation(self):
        current = self.overlay()
        incoming = dict(self.old, **{'VERSION': b'1.0.1\n'})
        entry, files, _ = self.plan(incoming, current)
        self.assertEqual(files['LICENSE'], current['LICENSE'])
        self.assertEqual(files['README.md'], current['README.md'])
        self.assertEqual(entry['migration_changes'], self.entry['migration_changes'])

    def test_simultaneous_edits_fail_without_merge(self):
        current = self.overlay()
        with self.assertRaisesRegex(ValueError, 'both changed'):
            self.plan(dict(self.old, **{'README.md': b'upstream docs\n'}), current)

    def test_deleted_local_overlay_fails(self):
        current = self.overlay()
        incoming = dict(self.old)
        del incoming['README.md']
        with self.assertRaisesRegex(ValueError, 'both changed'):
            self.plan(incoming, current)

    def test_untracked_or_modified_local_file_fails(self):
        for current in [dict(self.old, extra=b'unknown'), dict(self.old, **{'README.md': b'edited'})]:
            with self.assertRaisesRegex(ValueError, 'Unreviewed'):
                self.plan(current=current)

    def test_rewritten_baseline_fails(self):
        self.entry['source_sha256']['README.md'] = 'bad'
        with self.assertRaisesRegex(ValueError, 'provenance'):
            self.plan()

    def test_license_add_remove_change_requires_review(self):
        for incoming in [dict(self.old, LICENSE=b'Other license'), dict(self.old, NOTICE=b'Notice'), {p: b for p, b in self.old.items() if p != 'LICENSE'}]:
            with self.assertRaisesRegex(ValueError, 'License/notice'):
                self.plan(incoming)

    def test_paths_reject_escape_secrets_and_git_metadata(self):
        for path in ['../escape', '/absolute', 'a//b', '.git/config', 'x/.GiT/hooks', '.env', 'a/.env.test', 'id_rsa', 'node_modules/x', 'x\\y', 'x\ny']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                sync.safe_path(path)
        self.assertEqual(str(sync.safe_path('docs/install.md')), 'docs/install.md')

    def test_symlinks_and_submodules_fail(self):
        for mode, kind in [('120000', 'blob'), ('160000', 'commit')]:
            with mock.patch.object(sync, 'git', return_value=f'{mode} {kind} abc\tx\0'.encode()):
                with self.assertRaisesRegex(ValueError, 'Symlink/submodule'):
                    sync.snapshot(ROOT, 'a' * 40)

    def test_local_symlink_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / self.entry['path']
            package.mkdir(parents=True)
            (package / 'link').symlink_to('/tmp')
            with self.assertRaisesRegex(ValueError, 'symlink'):
                sync.current_files(root, self.entry)

    def test_full_sync_noop_leaves_checkout_untouched(self):
        # No network: clone/snapshot calls return controlled fixtures for all three sources.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entries = []
            for name, repository in sync.SOURCES.items():
                e = copy.deepcopy(self.entry)
                e.update(name=name, path='packages/' + name, source_url='https://github.com/' + repository)
                entries.append(e)
                base = root / e['path']
                base.mkdir(parents=True)
                for rel, payload in self.old.items():
                    (base / rel).write_bytes(payload)
            catalog = root / 'catalog.json'
            catalog.write_text(json.dumps({'schema_version': 1, 'packages': entries}))
            before = catalog.read_bytes()
            def fake_git(*args, **kwargs):
                return b'a' * 40 if args[0] == 'rev-parse' else b''
            with mock.patch.object(sync, 'git', side_effect=fake_git), mock.patch.object(sync, 'snapshot', return_value=(self.old, {p: 0o100644 for p in self.old})), mock.patch.object(sync, 'version', return_value='1.0.0'):
                self.assertEqual(sync.sync(root), [])
            self.assertEqual(catalog.read_bytes(), before)
            self.assertFalse((root / 'sync').exists())


    def test_full_sync_file_directory_transitions_and_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entries = []
            old = dict(self.old, **{'become-file/old.md': b'old', 'become-dir': b'old'})
            incoming = dict(self.old, **{'become-file': b'new file', 'become-dir/new.md': b'new child', 'ignored.log': b'tracked source log'})
            for name, repository in sync.SOURCES.items():
                e = copy.deepcopy(self.entry)
                e.update(name=name, path='packages/' + name, source_url='https://github.com/' + repository,
                         source_sha256={p: sync.digest(b) for p, b in old.items()},
                         current_sha256={p: sync.digest(b) for p, b in old.items()})
                entries.append(e)
                base = root / e['path']
                for rel, payload in old.items():
                    file = base / rel
                    file.parent.mkdir(parents=True, exist_ok=True)
                    file.write_bytes(payload)
            catalog = root / 'catalog.json'
            catalog.write_text(json.dumps({'schema_version': 1, 'packages': entries}))
            def fake_git(*args, **kwargs):
                return b'b' * 40 if args[0] == 'rev-parse' else b''
            def snapshots(repo, commit):
                files = old if commit == 'a' * 40 else incoming
                return files, {p: 0o100644 for p in files}
            with mock.patch.object(sync, 'git', side_effect=fake_git), mock.patch.object(sync, 'snapshot', side_effect=snapshots), mock.patch.object(sync, 'version', return_value='1.0.0'):
                report = sync.sync(root)
            self.assertEqual(len(report), 3)
            for e in entries:
                self.assertEqual(sync.current_files(root, e), incoming)
                history = root / 'sync/history' / e['name'] / ('a' * 40 + '.json')
                self.assertEqual(json.loads(history.read_text()), e)
            self.assertTrue(all(e['source_commit'] == 'b' * 40 for e in json.loads(catalog.read_text())['packages']))

    def test_later_source_failure_applies_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entries = []
            for name, repository in sync.SOURCES.items():
                e = copy.deepcopy(self.entry)
                e.update(name=name, path='packages/' + name, source_url='https://github.com/' + repository)
                entries.append(e)
                base = root / e['path']
                base.mkdir(parents=True)
                for rel, payload in self.old.items():
                    (base / rel).write_bytes(payload)
            catalog = root / 'catalog.json'
            catalog.write_text(json.dumps({'schema_version': 1, 'packages': entries}))
            before = catalog.read_bytes()
            def fake_git(*args, **kwargs):
                return b'b' * 40 if args[0] == 'rev-parse' else b''
            def snapshots(repo, commit):
                if repo.name == 'web-feature-demo':
                    raise ValueError('Later source failed')
                files = self.old if commit == 'a' * 40 else dict(self.old, **{'README.md': b'updated'})
                return files, {p: 0o100644 for p in files}
            with mock.patch.object(sync, 'git', side_effect=fake_git), mock.patch.object(sync, 'snapshot', side_effect=snapshots), mock.patch.object(sync, 'version', return_value='1.0.0'):
                with self.assertRaisesRegex(ValueError, 'Later source'):
                    sync.sync(root)
            self.assertEqual(catalog.read_bytes(), before)
            for e in entries:
                self.assertEqual(sync.current_files(root, e), self.old)
            self.assertFalse((root / 'sync').exists())


class PublishTests(unittest.TestCase):
    def run_main(self, report, api, git=None):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'report.json'
            path.write_text(json.dumps(report))
            with mock.patch.object(sys, 'argv', ['publish', '--report', str(path)]), mock.patch.object(publish, 'api', side_effect=api), mock.patch.object(publish, 'git', side_effect=git):
                publish.main()

    def test_noop_does_not_call_github(self):
        def reject(*args, **kwargs):
            self.fail('No-op must not call GitHub')
        self.run_main([], reject)

    def test_existing_pr_is_not_overwritten(self):
        calls = []
        def api(path, *args):
            calls.append(path)
            return [{'head': {'ref': 'sync/upstream-test'}, 'html_url': 'https://github.com/ChoMinGi/agent.d/pull/1'}]
        self.run_main([{'package': 'x'}], api)
        self.assertEqual(calls, ['pulls?state=open&per_page=100&page=1'])

    def test_moved_main_stops_without_writes(self):
        calls = []
        def api(path, *args):
            calls.append(path)
            return [] if path.startswith('pulls?') else {'object': {'sha': 'new'}}
        with self.assertRaisesRegex(SystemExit, 'main moved'):
            self.run_main([{'package': 'x'}], api, lambda *a: b'old')
        self.assertEqual(len(calls), 2)


    def test_existing_pr_on_page_two(self):
        calls = []
        def api(path, *args):
            calls.append(path)
            if path.endswith('page=1'):
                return [{'head': {'ref': 'unrelated'}}] * 100
            return [{'head': {'ref': 'sync/upstream-old'}, 'html_url': 'https://github.com/ChoMinGi/agent.d/pull/1'}]
        self.run_main([{'package': 'x'}], api)
        self.assertEqual(len(calls), 2)

    def test_publish_ignored_addition_deletion_modes_and_retry(self):
        import urllib.error
        for existing in (False, True):
            with self.subTest(existing=existing), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                file = root / 'packages/cognitive-partner/ignored.log'
                file.parent.mkdir(parents=True)
                file.write_bytes(b'new source file')
                file.chmod(0o755)
                calls = []
                def git(*args):
                    if args[0] == 'rev-parse':
                        return b'base'
                    if args[0] == 'diff':
                        return b'packages/cognitive-partner/deleted.txt\0'
                    return b'packages/cognitive-partner/ignored.log\0' if '--exclude-standard' not in args else b''
                def api(path, method='GET', data=None):
                    calls.append((path, method, data))
                    if path.startswith('pulls?'): return []
                    if path == 'git/ref/heads/main': return {'object': {'sha': 'base'}}
                    if path == 'git/commits/base': return {'tree': {'sha': 'base-tree'}}
                    if path == 'git/blobs': return {'sha': 'blob'}
                    if path == 'git/trees': return {'sha': 'new-tree'}
                    if path.startswith('git/ref/heads/sync/'):
                        if existing: return {'object': {'sha': 'prior'}}
                        raise urllib.error.HTTPError('test', 404, 'not found', {}, None)
                    if path == 'git/commits/prior': return {'tree': {'sha': 'new-tree'}, 'parents': [{'sha': 'base'}]}
                    if path == 'git/commits': return {'sha': 'new-commit'}
                    if path == 'git/refs': return {}
                    if path == 'pulls': return {'html_url': 'https://github.com/ChoMinGi/agent.d/pull/1'}
                    raise AssertionError(path)
                report = [{'package': 'cognitive-partner', 'from': 'a' * 40, 'to': 'b' * 40, 'compare': 'https://github.com/ChoMinGi/cognitive-partner/compare/a...b', 'added': ['ignored.log'], 'removed': ['deleted.txt'], 'changed': []}]
                with mock.patch.object(publish, 'ROOT', root):
                    self.run_main(report, api, git)
                tree = next(data['tree'] for path, method, data in calls if path == 'git/trees')
                self.assertEqual(tree, [
                    {'path': 'packages/cognitive-partner/deleted.txt', 'mode': '100644', 'type': 'blob', 'sha': None},
                    {'path': 'packages/cognitive-partner/ignored.log', 'mode': '100755', 'type': 'blob', 'sha': 'blob'}])
                self.assertEqual(sum(path == 'git/refs' for path, _, _ in calls), 0 if existing else 1)
                self.assertTrue(next(data['draft'] for path, _, data in calls if path == 'pulls'))
                self.assertFalse(any(method in {'PATCH', 'PUT', 'DELETE'} for _, method, _ in calls))


if __name__ == '__main__':
    unittest.main()

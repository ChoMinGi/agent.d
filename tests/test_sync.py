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
        self.assertEqual(calls, ['pulls?state=open&per_page=100'])

    def test_moved_main_stops_without_writes(self):
        calls = []
        def api(path, *args):
            calls.append(path)
            return [] if path.startswith('pulls?') else {'object': {'sha': 'new'}}
        with self.assertRaisesRegex(SystemExit, 'main moved'):
            self.run_main([{'package': 'x'}], api, lambda *a: b'old')
        self.assertEqual(len(calls), 2)


if __name__ == '__main__':
    unittest.main()

import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('release_check', ROOT / 'scripts/release_check.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def test_sensitive_content_is_rejected(self):
        samples = ['nt' + 'n_' + 'a' * 25, 'https://' + 'notion.so/' + 'private-page',
                   'https://' + 'app.notion.com/' + 'private-page',
                   '/' + 'Users' + '/someone/private.json',
                   '-----BEGIN ' + 'PRIVATE KEY-----']
        for sample in samples:
            with self.subTest(sample=sample), self.assertRaises(ValueError):
                release.scan_content('fictional-test.txt', sample)

    def test_traversal_private_paths_and_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'safe.md').write_text('Fictional public file')
            for entry in ('../outside.md', '/etc/passwd', 'private/export.json'):
                (root / 'MANIFEST.txt').write_text(entry)
                with self.subTest(entry=entry), self.assertRaises(ValueError):
                    release.public_files(root)
            (root / 'link.md').symlink_to(root / 'safe.md')
            (root / 'MANIFEST.txt').write_text('link.md')
            with self.assertRaises(ValueError):
                release.public_files(root)

    def test_package_contains_only_manifest_files_and_is_reproducible(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'public.md').write_text('Fictional public document')
            (root / 'unlisted-private.md').write_text('Never package this file')
            first = root / 'one.zip'
            second = root / 'two.zip'
            a = release.package(root, ['public.md'], first)
            b = release.package(root, ['public.md'], second)
            self.assertEqual(a, b)
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(set(archive.namelist()),
                                 {'decisionguard/public.md', 'decisionguard/SHA256SUMS.json'})

    def test_package_cannot_overwrite_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'source.md').write_text('Keep this source')
            with self.assertRaises(ValueError):
                release.package(root, ['source.md'], root / 'source.md')
            self.assertEqual((root / 'source.md').read_text(), 'Keep this source')

    def test_recording_cannot_depend_on_unpackaged_or_changed_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / 'examples/demo'
            folder.mkdir(parents=True)
            evidence = folder / 'plan.md'
            evidence.write_text('Fictional reviewed plan')
            (folder / 'file-hashes.json').write_text(json.dumps({'plan.md': hashlib.sha256(evidence.read_bytes()).hexdigest()}))
            entries = ['examples/demo/file-hashes.json']
            with self.assertRaisesRegex(ValueError, 'missing from manifest'):
                release.validate_recording_files(root, entries)
            entries.append('examples/demo/plan.md')
            release.validate_recording_files(root, entries)
            evidence.write_text('Changed after sealing')
            with self.assertRaisesRegex(ValueError, 'recording changed'):
                release.validate_recording_files(root, entries)


if __name__ == '__main__':
    unittest.main()

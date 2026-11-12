"""Offline installation, archive and boundary checks for the monorepo."""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from install_skill import install
from package_skill import build
from skill_common import catalog, runtime_files, safe_relative
from verify_monorepo import validate


class IntegrationTests(unittest.TestCase):
    def test_repository_integrity(self):
        result = validate()
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(result['imported_files'], 240)

    def test_migration_notes_match_changed_files(self):
        for entry in catalog():
            changed = {rel for rel in entry['source_sha256']
                       if entry['source_sha256'][rel] != entry['current_sha256'][rel]}
            self.assertEqual(changed, set(entry['migration_changes']))
            self.assertTrue(all(entry['migration_changes'][rel].strip() for rel in changed))
            if entry['name'] != 'cognitive-partner':
                self.assertEqual(changed, set())

    def test_runtime_behavior_and_license_preservation(self):
        for entry in catalog():
            _, files = runtime_files(entry['name'])
            for relative, path in files.items():
                source_relative = str(path.relative_to(ROOT / entry['path']))
                if relative != 'LICENSE':
                    self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                                     entry['source_sha256'][source_relative])
            self.assertTrue(files['LICENSE'].read_text().startswith('MIT License'))
        self.assertIn('DecisionGuard contributors', (ROOT / 'packages/decisionguard/LICENSE').read_text())
        self.assertIn('web-feature-demo contributors', (ROOT / 'packages/web-feature-demo/LICENSE').read_text())

    def test_independent_installs(self):
        with tempfile.TemporaryDirectory() as tmp:
            for entry in catalog():
                name = entry['name']
                destination = Path(tmp).resolve() / name
                result = install(name, destination)
                _, source_files = runtime_files(name)
                self.assertEqual(set(result), set(source_files))
                self.assertEqual({str(p.relative_to(destination)) for p in destination.rglob('*') if p.is_file()}, set(source_files))
                for relative, original in source_files.items():
                    self.assertEqual((destination / relative).read_bytes(), original.read_bytes())
                self.assertTrue((destination / 'LICENSE').is_file())
                self.assertTrue((destination / 'SKILL.md').is_file())
                if name != 'web-feature-demo':
                    self.assertFalse((destination / 'evals').exists())
                    self.assertFalse((destination / 'examples').exists())
                before = (destination / 'SKILL.md').read_bytes()
                with self.assertRaises(ValueError):
                    install(name, destination)
                self.assertEqual((destination / 'SKILL.md').read_bytes(), before)

    def test_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp).resolve() / 'decisionguard'
            self.assertTrue(install('decisionguard', destination, dry_run=True))
            self.assertFalse(destination.exists())

    def test_symlink_and_name_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp).resolve()
            (parent / 'target').mkdir()
            (parent / 'decisionguard').symlink_to(parent / 'target', target_is_directory=True)
            with self.assertRaises(ValueError):
                install('decisionguard', parent / 'decisionguard')
            (parent / 'alias').symlink_to(parent / 'target', target_is_directory=True)
            with self.assertRaises(ValueError):
                install('decisionguard', parent / 'alias/decisionguard')
            with self.assertRaises(ValueError):
                install('decisionguard', parent / 'wrong-name')
            self.assertEqual(list((parent / 'target').iterdir()), [])

    def test_invalid_skill_and_paths(self):
        with self.assertRaises(ValueError):
            runtime_files('missing-skill')
        for value in ('/tmp/outside', '../outside', 'folder/../../outside', '', 'a//b'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_relative(value)

    def test_reproducible_archives(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp).resolve()
            for entry in catalog():
                name = entry['name']
                first, second = parent / (name + '-a.zip'), parent / (name + '-b.zip')
                build(name, first)
                build(name, second)
                self.assertEqual(first.read_bytes(), second.read_bytes())
                _, originals = runtime_files(name)
                with zipfile.ZipFile(first) as archive:
                    self.assertIsNone(archive.testzip())
                    self.assertEqual(set(archive.namelist()), {name + '/' + rel for rel in originals})
                    for rel, original in originals.items():
                        self.assertEqual(archive.read(name + '/' + rel), original.read_bytes())
                before = hashlib.sha256(first.read_bytes()).hexdigest()
                with self.assertRaises(ValueError):
                    build(name, first)
                self.assertEqual(hashlib.sha256(first.read_bytes()).hexdigest(), before)

    def test_cli_from_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp).resolve() / 'cognitive-partner'
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/install_skill.py'), '--skill', 'cognitive-partner', '--dest', str(dest)], cwd=tmp, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((dest / 'SKILL.md').is_file())


if __name__ == '__main__':
    unittest.main()

"""Local manifest-based package access. No network or publication."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def safe_relative(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or '..' in path.parts or str(path) != value:
        raise ValueError(f'Unsafe relative path: {value}')
    return path


def no_symlinks(path):
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise ValueError(f'Symlink is not supported: {candidate}')


def catalog():
    no_symlinks(ROOT / 'catalog.json')
    result = json.loads((ROOT / 'catalog.json').read_text())
    if result.get('schema_version') != 1:
        raise ValueError('Unsupported catalog version')
    names = [item['name'] for item in result['packages']]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate skill names')
    return result['packages']


def package(name):
    entries = [entry for entry in catalog() if entry['name'] == name]
    if len(entries) != 1:
        raise ValueError(f'Unknown skill: {name}')
    entry = entries[0]
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', entry['name']):
        raise ValueError('Invalid skill name')
    base = ROOT / safe_relative(entry['path'])
    no_symlinks(base)
    if not base.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Package escaped repository')
    original = entry['source_sha256']
    current = entry.get('current_sha256', original)
    if set(current) != set(original):
        raise ValueError('Imported file inventory must remain explicit')
    changed = {rel for rel in original if original[rel] != current[rel]}
    if changed != set(entry.get('migration_changes', {})):
        raise ValueError('Every migration change must be documented')
    for rel, expected in current.items():
        source = base / safe_relative(rel)
        no_symlinks(source)
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Package differs from reviewed source: {entry["name"]}/{rel}')
    return entry, base


def runtime_files(name):
    entry, base = package(name)
    prefix = entry['skill_path']
    if prefix != '.':
        safe_relative(prefix)
    result = {}
    for relative in entry['source_sha256']:
        if prefix == '.':
            dest = relative
        elif relative.startswith(prefix + '/'):
            dest = relative[len(prefix) + 1:]
        else:
            continue
        safe_relative(dest)
        result[dest] = base / relative
    result['LICENSE'] = base / 'LICENSE'
    if 'SKILL.md' not in result:
        raise ValueError('Runtime SKILL.md missing')
    return entry, dict(sorted(result.items()))

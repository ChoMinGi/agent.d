#!/usr/bin/env python3
"""Build one reproducible skill ZIP, including its package license; no upload."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from skill_common import no_symlinks, runtime_files


def build(name, output):
    entry, files = runtime_files(name)
    output = Path(output).expanduser().absolute()
    no_symlinks(output)
    if output.exists():
        raise ValueError('Archive already exists; refusing overwrite')
    if not output.parent.is_dir():
        raise ValueError('Create the archive parent directory first')
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, source in files.items():
            info = zipfile.ZipInfo(name + '/' + relative, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o100755 if source.stat().st_mode & 0o111 else 0o100644
            info.external_attr = mode << 16
            archive.writestr(info, source.read_bytes())
    return {'skill': name, 'version': entry['version'], 'files': len(files),
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.skill, args.out), indent=2))
    except (ValueError, OSError) as exc:
        print(f'package-skill: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())

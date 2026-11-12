#!/usr/bin/env python3
"""Copy one reviewed skill into an explicit, new directory; never overwrite."""
import argparse
import os
from pathlib import Path
import sys
from skill_common import no_symlinks, runtime_files


def install(name, destination, dry_run=False):
    entry, files = runtime_files(name)
    destination = Path(os.path.abspath(Path(destination).expanduser()))
    no_symlinks(destination)
    if destination.name != entry['name']:
        raise ValueError('Destination directory must be named ' + entry['name'])
    if destination.exists():
        raise ValueError('Destination already exists; inspect and back it up first')
    if not destination.parent.is_dir():
        raise ValueError('Create the destination parent directory first')
    if dry_run:
        return list(files)
    # Exclusive mkdir refuses an existing destination even if it appeared after preflight.
    # On I/O failure retain the partial directory for inspection instead of deleting data.
    destination.mkdir()
    for relative, source in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        no_symlinks(target)
        with target.open('xb') as handle:
            handle.write(source.read_bytes())
        target.chmod(0o755 if source.stat().st_mode & 0o111 else 0o644)
    return list(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill', required=True)
    parser.add_argument('--dest', type=Path, required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        names = install(args.skill, args.dest, args.dry_run)
        print(('Would install' if args.dry_run else 'Installed') + f' {args.skill}: {len(names)} files at {args.dest}')
        if args.dry_run:
            print('\n'.join(names))
    except (ValueError, OSError) as exc:
        print(f'install-skill: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())

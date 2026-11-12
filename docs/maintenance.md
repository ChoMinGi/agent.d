# Structure and maintenance

```text
agent.d/
  README.md
  catalog.json
  LICENSE.md
  packages/
    cognitive-partner/   # full upstream repository snapshot
    decisionguard/       # full upstream repository snapshot
    web-feature-demo/    # full upstream repository snapshot
  scripts/              # local install, archive, and integrity checks
  tests/                # monorepo integration tests
  docs/
```

## Source preservation

This migration imports the tracked files of each current `main` snapshot, including documentation, examples and tests. No `.git` directories, local environments, working data, credentials or untracked outputs were copied. Package files are byte-for-byte preserved; the root catalog records every source file hash and the exact source commit.

The original repositories, issues, tags, release assets and installation URLs remain unchanged. Original Git history is not rewritten or imported. This keeps old links working and avoids exposing unrelated historical content. It is a snapshot migration, not a history-preserving merge. Nothing here deletes, archives or redirects the originals.

Package-level instructions run from their package directory. The root installer resolves paths relative to its own file, not the shell's working directory. All three runtime SKILL.md files retain their original names and references.

## Independent versions

- Cognitive Partner: 1.0.0
- DecisionGuard: 0.6.1
- Web Feature Demo: 1.0.0

These are source package versions, not a shared monorepo version. Future releases can use tags such as `cognitive-partner/v1.0.1`, `decisionguard/v0.6.2`, and `web-feature-demo/v1.0.1`. These examples have not been created. Preserve old repository tags and avoid making consumers upgrade unrelated skills.

`catalog.json` locks the current imported sources. To update a package, review the incoming commit, preserve its license and provenance records, update that package's catalog entry and hashes, then run all affected checks. Do not treat a hash update as review or license approval.

## Validation

```sh
python3 -B scripts/verify_monorepo.py
python3 -B -m unittest discover -s tests -v
```

These checks include original-byte integrity, file inventory, local Markdown targets, versions, skill names, obvious secret patterns, independent installation and ZIP contents. They do not run real models or prove product effectiveness.

Run each package's own tests from its directory as well. Cognitive Partner requires the `requirements-dev.txt` dependency. Web Feature Demo's full tests require Chrome and a Playwright runner and may open test windows. See [verification](verification.md) for actual results rather than assuming these commands were run.

## Public release checklist

1. Confirm creation and visibility of `ChoMinGi/agent.d` with the owner. No remote is configured by this preparation.
2. Ask the owner to select Cognitive Partner's license and any root-content license. Do not apply MIT to the entire tree by inference. Existing MIT notices must remain intact.
3. Confirm rights in source media and contributed material; inspect the exact files to be uploaded. Repeat secret/privacy review after any edit.
4. Run package tests and root integration checks against the release tree. Check archive names, licenses, and extracted content.
5. Create/push/tag only within explicit authorization. Verify the exact remote commit and checks before reporting publication.

Suggested repository About: `Personal agent skills for critical thinking, project decisions, and local browser demos.`

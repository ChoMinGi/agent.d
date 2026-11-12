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

This migration imports the tracked files of each current `main` snapshot, including documentation, examples and tests. No `.git` directories, local environments, working data, credentials or untracked outputs were copied. Runtime files and evaluation materials are byte-for-byte preserved. Cognitive Partner's license and related documentation were updated with owner approval. The root catalog retains every original source hash and exact source commit separately from reviewed current hashes and documented migration changes.

The original repositories, issues, tags, release assets and installation URLs remain unchanged. Original Git history is not rewritten or imported. This keeps old links working and avoids exposing unrelated historical content. The initial migration was a snapshot import, not a history-preserving merge. The [one-way synchronization workflow](sync.md) now provides reviewed updates from those original repositories once activated. Nothing here deletes, archives or redirects the originals.

Package-level instructions run from their package directory. The root installer resolves paths relative to its own file, not the shell's working directory. All three runtime SKILL.md files retain their original names and references.

## Independent versions

- Cognitive Partner: 1.0.0
- DecisionGuard: 0.6.1
- Web Feature Demo: 1.0.0

These are source package versions, not a shared monorepo version. Future releases can use tags such as `cognitive-partner/v1.0.1`, `decisionguard/v0.6.2`, and `web-feature-demo/v1.0.1`. These examples have not been created. Preserve old repository tags and avoid making consumers upgrade unrelated skills.

`catalog.json` locks the current source snapshots and reviewed current package files. Automatic updates retain superseded source records in `sync/history/`; original Git history remains in the original repositories. To update a package, review the incoming commit, preserve its license and provenance records, update that package's catalog entry, current hashes and change notes, then run all affected checks. Do not treat a hash update as review or license approval.

## Validation

```sh
python3 -B scripts/verify_monorepo.py
python3 -B -m unittest discover -s tests -v
```

These checks include reviewed-byte integrity and original source provenance, file inventory, local Markdown targets, versions, skill names, obvious secret patterns, independent installation and ZIP contents. They do not run real models or prove product effectiveness.

Run each package's own tests from its directory as well. Cognitive Partner requires the `requirements-dev.txt` dependency. Web Feature Demo's full tests require Chrome and a Playwright runner and may open test windows. See [verification](verification.md) for actual results rather than assuming these commands were run.

## Publication and future releases

The owner approved public `ChoMinGi/agent.d` and MIT for Cognitive Partner. The root MIT license covers agent.d integration code; the other packages retain their original MIT notices. The original repositories are not changed by this publication.

Before each later release:

1. Review exact changes, media and credential/privacy checks.
2. Run package tests and root integration checks against the release tree.
3. Keep per-package versions and license notices intact. Validate extracted archives.
4. Push or publish only within the owner's current authorization. Verify the exact remote commit and CI result.

Do not run the imported Cognitive Partner `scripts/publish.sh` to publish this monorepo: it describes the original standalone repository and tag. Use root Git operations targeting `ChoMinGi/agent.d`.

The validation workflow in `.github/workflows/validate.yml` and its [original example](ci.example.yml) cover root integration, Cognitive Partner and DecisionGuard checks, plus JavaScript/shell syntax checks. See [activation requirements](sync.md#activation-requirements) before assuming the workflows are enabled, and verify the run for the exact commit. Full Chrome UI/lifecycle checks were run locally; the example does not claim browser coverage.

Repository About: `Personal agent skills for critical thinking, project decisions, and local browser demos.`

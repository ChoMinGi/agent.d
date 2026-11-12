# One-way upstream synchronization

The original repositories remain the source of truth:

- `ChoMinGi/cognitive-partner` → `packages/cognitive-partner`
- `ChoMinGi/decisionguard-skill` → `packages/decisionguard`
- `ChoMinGi/claude-code-web-feature-demo-skill` → `packages/web-feature-demo`

Once enabled on `main`, **Sync upstream skills** checks each original `main` at minute 17 of every hour, and supports manual runs. GitHub may delay scheduled runs. Public repositories with no repository activity for 60 days can have schedules disabled by GitHub; re-enable the workflow if that happens. No webhook, personal access token, original-repository workflow, or laptop is needed.

## What is automatic

New source commits produce a **draft pull request**, with source commit links, changed/added/deleted files, package versions and updated SHA-256 records. Review and merge are manual. Nothing writes back to an original repository, creates releases/tags, or auto-merges into `agent.d/main`.

If an upstream sync PR is already open, it is left untouched. After it is merged or closed, a later run proposes any remaining changes. This avoids force-pushing over reviews or manual fixes. Concurrent `main` changes cause a safe failure; the next scheduled run starts from fresh `main`. Failed PR creation can leave an immutable `sync/upstream-*` branch; a retry reuses it only when its exact parent and tree match. No branch is deleted or force-pushed.

A no-change run creates no commit or PR. Source updates only appear in the installable `agent.d/main` after their PR is merged. This is not an instant push mirror or a two-way sync.

## Safety and provenance

- Only the three hard-coded public repositories and their `main` branches are read. Only their corresponding package directories and provenance records may be changed.
- The importer reads Git blobs as data. It does not check out or execute source hooks, scripts, workflows, dependency installs, submodules or filters.
- Source commit ancestry and the previous source hashes must match. Rewritten history stops the import.
- Current package contents must match the catalog, including file inventory. Local edits, extra files, symlinks, path traversal, probable credential filenames, oversized files and unsupported Git entries stop the import.
- Upstream deletions remove only previously recorded package files. Empty directories are cleaned up. Normal additions and updates are included.
- The approved Cognitive Partner MIT notice and publication-documentation changes are retained. If upstream edits or removes a locally changed file, the job stops for manual resolution rather than guessing which version wins.
- Changes to upstream license/copyright notice files require manual review. A catalog hash update is never license approval.
- Every superseded catalog entry is retained under `sync/history/<package>/<source-commit>.json`. The active catalog identifies the current source commit, source hashes, actual imported hashes, versions and any retained migration differences.
- Limited secret-pattern and local-link checks run before publication. They are not a full security, privacy or rights audit.

## Workflows and permissions

`sync-upstream.yml` needs `contents: write` and `pull-requests: write` for **agent.d only**. The token is passed only to the trusted PR publisher, after static/integration tests. Checkout does not persist credentials. Upstream code is never executed in this write-capable job. The publisher uses GitHub's Git Data API, creates a new immutable branch and draft PR, and does not merge or approve.

`validate.yml` has `contents: read`, no repository secrets, and no persisted checkout credentials. It runs package validators/tests and syntax checks on pushes, pull requests, or manually selected branches. Browser/Chrome lifecycle checks are not included.

GitHub usually suppresses follow-on workflow triggers for events created with `GITHUB_TOKEN`. Therefore a bot-created sync PR may not get an automatic PR validation run. Before merging, run **Validate skills → Run workflow** on its `sync/upstream-*` branch, or close/reopen the PR yourself. The sync job's static/install/archive tests already ran, but do not replace package validation.

## Activation requirements

1. Commit both files in `.github/workflows/` through a connection authorized to write workflows. A GitHub CLI OAuth login generally needs the `workflow` scope; do not broaden credentials silently.
2. Merge the reviewed setup into `main`. Scheduled workflows only run from the default branch.
3. In **Settings → Actions → General → Workflow permissions**, allow GitHub Actions to create and approve pull requests. The workflow only creates drafts and never uses approval. Leave default workflow permissions read-only; the sync job requests its two necessary permissions explicitly.
4. Run **Validate skills** and **Sync upstream skills** manually and verify the exact run/commit. A successful no-change run is expected until an original repository changes.

Do not describe synchronization as enabled until the workflow is on `main` and its run and PR permission are verified. These setup steps may require owner approval or a browser handoff, depending on available credentials.

## Local preparation and tests

Use a clean isolated clone. The importer updates that clone but never pushes:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/sync_upstream.py --report /tmp/agent-d-sync-report.json
python3 -B scripts/verify_monorepo.py
python3 -B -m unittest discover -s tests -v
```

The report must live outside the checkout. Review changes before publishing. `publish_sync_pr.py` is intended for the workflow; it needs `GH_TOKEN` and only targets `ChoMinGi/agent.d`.

If a safety check fails, inspect the workflow logs, compare source commits and resolve the issue in a reviewed PR. Do not disable the check, replace the original provenance, overwrite local changes, or automatically accept a changed license just to make the job green.

# Maintainer release checks

DecisionGuard is published as an experimental alpha at
[ChoMinGi/decisionguard-skill](https://github.com/ChoMinGi/decisionguard-skill).
The first public tag is `v0.6.1`. Installation and usage are documented separately
in [install.md](install.md) and [walkthrough.md](walkthrough.md).

## Scope and privacy

`MANIFEST.txt` explicitly lists distributable files. The packager never walks
parent folders or includes Git history. Private exports, project memory, receipts,
reports, credentials and local paths must stay outside this repository. Examples
must be authored as fiction; anonymizing a real export is not sufficient.

Inspect content even when automated checks pass. Pattern matching does not detect
every private fact. Also review staged filenames, the full staged diff and commit
identity before a push. GitHub's no-reply email can avoid publishing a personal email.

## Validate

From the repository root:

```sh
python3 -B -m unittest discover -s tests
python3 -B scripts/evaluate_context.py
python3 -B scripts/evaluate_raw_context.py
python3 -B scripts/evaluate_context_v2.py
python3 -B scripts/evaluate_handoff.py
python3 -B scripts/evaluate_blind_context.py --compact
python3 -B scripts/release_check.py --require-git
python3 -B scripts/release_check.py --zip dist/decisionguard-v0.6.1.zip
```

The archive contains only manifest files and `SHA256SUMS.json`. Fixed timestamps
make packaging reproducible on the same Python/zlib environment. The checker
verifies basic skill metadata, references, sealed recordings and privacy patterns.
When the host provides `skill-creator`, its `quick_validate.py` can also validate
the installed skill; that external tool needs PyYAML. Shipped helpers and tests
have no third-party Python dependencies.

GitHub Actions is not enabled in the initial publication. The
[optional workflow example](ci.example.yml) targets Python 3.10 and 3.13 with
read-only repository permissions. Its package step builds locally in the runner;
it does not publish releases or workspace data. To enable it, a maintainer with
permission to publish workflow files can copy it to `.github/workflows/ci.yml`,
update the manifest and run the checks before pushing. Do not report hosted CI as
passed until an actual run completes.

## Publish a deliberate version

Publish only the reviewed commit and archive. Use an alpha/prerelease label until
there is evidence supporting broader readiness. The release notes should distinguish
intended behavior, deterministic tests, recorded fictional runs and unmeasured
real-world outcomes. Do not advertise reduced user effort or accuracy gains
without appropriate evidence.

Keep old tags and sealed example recordings unchanged. Repository publishing and
release creation use the maintainer's existing GitHub authentication; this project
contains no publishing token or automatic release job. Prefer private vulnerability
reporting for sensitive issues and keep ordinary reproductions fictional.

References: [skill installation](https://learn.chatgpt.com/docs/build-skills),
[GitHub checkout](https://github.com/actions/checkout),
[GitHub Python setup](https://github.com/actions/setup-python).

# Verification

Checked on 2026-11-12 on macOS with Python 3.13.2, PyYAML 6.0.3, Node.js 26.5.0 and installed Google Chrome. Tests are local/deterministic; no real model evaluation or project-effectiveness claim is made.

## Source snapshot

| Package | Version | Imported main commit | Files |
| --- | --- | --- | --- |
| Cognitive Partner | 1.0.0 | `b35679f2d40cd64b5b812dd6f36552c23745c452` | 33 |
| DecisionGuard | 0.6.1 | `eb571b677512ec611f06eea043b12544b69d62c6` | 175 |
| Web Feature Demo | 1.0.0 | `38afa6f7fb5c1b9f0e500ad9cbca5588dee722c8` | 32 |

Each source was clean and matched its remote `main` when inspected. All 240 tracked source files were imported byte-for-byte. `catalog.json` records their SHA-256 digests. Original working copies and remote repositories were left unchanged.

## Passed checks

- Root integrity validator: 240 original file hashes and exact package inventories, three skill names and versions, 105 local Markdown link paths, and limited credential-pattern scans.
- Seven root integration tests: independent installation into temporary directories; expected runtime files and LICENSE; exclusion of Cognitive Partner evaluation answers and DecisionGuard evaluation fixtures; existing installation preservation; symlink/name/traversal refusal; dry-run; deterministic per-skill ZIPs and CRC/content verification; CLI invocation from an unrelated working directory.
- Cognitive Partner: 153 static checks, 158/158 validator contract tests, release provenance and inventory checks. Report-writing validators ran on a temporary copy so the source snapshot stayed intact.
- DecisionGuard: 149/149 unit tests; five evaluation/replay scripts; release check for all 175 public manifest files. The replay scripts validate saved synthetic evidence, not new model outputs.
- Web Feature Demo: 10 JavaScript and 2 shell syntax checks; full Chrome smoke suite including sample scenes, login/cleanup tests, three login modes, missing-element handling, external HTTP and WebSocket blocking; all five lifecycle cases (SIGINT, SIGTERM, close, timeout, keep). The sample server was stopped afterward.
- Two source PNG examples were visually inspected: synthetic UI, no apparent personal content.

Each independent ZIP includes its original LICENSE and installs under its unchanged skill name. ZIP output was generated twice in isolated tests and matched byte-for-byte.

## Limitations and release decisions

- No host-level Codex/Claude skill activation or real user model session was tested. Installation checks validate files and paths, not host discovery or behavior.
- WebM example videos were retained byte-for-byte but were not visually audited. A media rights/privacy review remains appropriate before a new public release.
- Pattern scans found no actual credentials in the imported files, but cannot guarantee absence of secrets or prove ownership. Source provenance is not a legal rights audit.
- Cognitive Partner has no reuse/redistribution license yet. Root content has no newly selected license. DecisionGuard and Web Feature Demo retain MIT. Do not describe the whole monorepo as MIT or open source without the owner's license decision.
- No GitHub repository was created, no remote configured, no push/tag/release performed, and no existing repository was archived or redirected.
- No global skill installation, global instruction change, or user cache replacement was performed. Browser test dependencies and reports stayed in isolated temporary storage.

## Reproduce

From the monorepo root:

```sh
python3 -B scripts/verify_monorepo.py
python3 -B -m unittest discover -s tests -v
```

Then follow each package README from its own directory to run its suite. Review the source catalog and package license notices before distributing artifacts.

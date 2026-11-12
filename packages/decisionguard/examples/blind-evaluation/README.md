# Blind-study recordings

These fictional fixtures were authored by a separate agent and hidden answer keys
were withheld from four fresh extractors until their outputs were sealed. The
answers are public here only **after** the study. Do not give them or the recorded
responses to an extractor when claiming a fresh blind run.

Read [the study and limitations](../../docs/blind-evaluation.md) and
[case totals](results.json). `experiment.json` records roles, freeze order and the
post-trial patch. Original skill file hashes identify the baseline and candidate.

For each suite:

- `documents.json`, `requests.json`, `raw/`: untagged source input and natural tasks.
- `answers.json`, `author-notes.md`: unchanged author labels and fair interpretation notes.
- `baseline-*`: sealed v0.3.0 outputs and separate scoring/adjudication.
- `improved-*`: sealed v0.4.0 candidate outputs and separate scoring/adjudication.
- `final-packets.json`: v0.4.1 replay of the same improved response after a diagnostic correction.

First responses are retained even when the extractor later narrowed an unsupported
title or fixed a validation error. Source and answer bytes were checked against
the author's pre-extraction manifest. `file-hashes.json` protects these packaged
recordings from accidental modification; it is not an external signature.

Raw logs containing local machine paths remain outside the distribution. Semantic
adjudications replace those path prefixes with relative logical paths. No real
Notion documents, credentials or personal workspace data appear in this study.

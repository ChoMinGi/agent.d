# Separate-author blind evaluation — 2026-11-08

Two new fictional projects exposed real context-selection failures in v0.3.0.
After changes based only on suite A, fresh extractors recovered all required
meanings and removed confirmed wrong selections on both A and held-out B.
A new classification-based warning regression was found and corrected afterward.
Original trial outputs and answer files are retained unchanged.

## What was blinded

An author agent with no inherited conversation and no access to the repository,
previous examples or implementation created both suites and answer keys. Each
suite has seven documents, three natural-language task requests, and a different
project/domain: vegetable-box substitution approval and offline field observations.
Six documents per suite are in scope; the seventh is another project. Each job
exposes 24 passages, including headings. Inputs contain provenance, not task-type
or topic annotations. There are 37 and 35 authored fact labels respectively.

Both input/answer sets were hashed before any extractor finished. Four fresh
extractor contexts received only an isolated copy of the skill and raw input:
baseline A/B using v0.3.0, then improved A/B using the frozen v0.4.0 candidate.
Each extraction produced three packets: four model runs, twelve task packets,
six unique task/corpus combinations. No answer keys, prior responses or scores
were given to an extractor. First responses were preserved before corrections.
Corrections used only source text or helper validation; no answer feedback.

The implementer inspected A to make the changes. B's contents, answers and
baseline results remained unopened by the implementer until the improvement
was frozen. Two separate reviewer contexts then compared each suite's outputs
with its frozen answers and source meaning. They did not change answer keys.

This is procedural blinding using fresh contexts, folder-scoped instructions,
read logs and hashes. Agents share a filesystem; it is not OS-enforced isolation.
All agents use the same configured agent service/family; this is role separation,
not a cross-model or population study. Source dates are fictional document dates;
freeze ordering is established by the orchestration and hash receipts.

## Results after semantic adjudication

Required facts are counted per request, not per output record: one record may
cover several facts, and one fact may be relevant to multiple requests.

| Suite / task | Required facts | Missing before → trial after | Wrong selections before → trial after |
| --- | ---: | ---: | ---: |
| A · market research | 12 | 2 → 0 | 2 → 0 |
| A · feature design | 15 | 0 → 0 | 2 → 0 |
| A · QA review | 15 | 0 → 0 | 4 → 0 |
| B · market research | 9 | 0 → 0 | 0 → 0 |
| B · feature design | 16 | 0 → 0 | 0 → 0 |
| B · QA review | 17 | 0 → 0 | 2 → 0 |

The improved trial covers **84/84 required fact/request pairs**, with zero
confirmed missing facts, wrong selections or domain-meaning distortions in this
small study. This is a case count, not a general accuracy estimate. Some relevance
judgments are subjective: A's two research extras were rated medium confidence.
Reviewers accepted useful source-backed extras on B rather than forcing arbitrary
packet sizes. A's research packet grew from 19 to 27 records while becoming more
relevant; shorter is not automatically better.

The raw anchor scorer initially found four missing research facts in A. Review
confirmed two named competitor observations were lost entirely; two limitations
were adequately disclosed in gaps, though their individual cited records were
absent. Enum differences such as `observed` test failure versus `open` defect,
and faithful clause splits, were explicitly waived. These waivers are preserved
in per-run adjudications; raw scorer failures are not silently changed to pass.

## Failures and changes

1. **A truncated tail erased intact observations.** The extractor had read and
   correctly extracted competitor observations, but `complete=false` made the
   selector discard every record from that document. Bounded observed excerpts
   and explicit unknowns can now survive with a cited completeness boundary and
   visible gap. Accepted authority cannot use this exception.
2. **Old sketches remained live context.** Later accepted choices and scope
   exclusions were selected alongside obsolete draft alternatives. The skill
   now reconciles all proposals/requests/sketches, with grounded cross-document
   status links, not only records called decisions. The current exclusion stays
   useful; the discarded proposal no longer occupies an active context slot.
3. **Topics and kinds were too broad.** Functional QA received a future interview
   question and an untested retention/response benefit. New raw extractions give
   each record an include/exclude judgment for the actual task with a reason.
   Project/scope, inactive state, evidence and budget gates remain in force.
   Cited prerequisites and competing accepted choices cannot be hidden by a
   relevance exclusion. Legacy normalized responses keep the existing fallback.
4. **Scheduled tests looked missing.** A test case could not be labeled planned,
   so faithful unexecuted plans received a false missing-test-context warning.
   `test_case/planned` now fills the plan-context slot and explicitly remains
   unexecuted. It never becomes a passing result.

## Regression found after the improved blind runs

The fresh extractors classified implementation rules as accepted decisions or
requirements. Both design packets then falsely reported missing `design` context,
despite preserving all required implementation meanings. Thus diagnostic errors
were **2 before → 2 in the frozen improved trial**, moving from QA to design.
The blind trial was not wholly clean; this regression is retained in its reports.

The final v0.4.1 patch treats absent `design` classification as a caution when
accepted decisions/requirements are available, asking the host to review their
implementation coverage. It does not claim semantic completeness. With no such
accepted evidence, the missing-context gap remains. This patch was replayed on
the same sealed responses; **all selected records stayed identical** and both
false absence warnings were removed. No fresh blind model run was performed for
this last diagnostic patch. Final packets are separate from the trial packets.

## Artifacts and reproduction

See [experiment metadata](../examples/blind-evaluation/experiment.json),
[case totals](../examples/blind-evaluation/results.json),
[suite A](../examples/blind-evaluation/suite-a/documents.json), and
[suite B](../examples/blind-evaluation/suite-b/documents.json). Each suite includes
raw prose, frozen answers/author notes, first and final extraction responses,
baseline/trial packets, raw scores and independent adjudications. `final-packets`
contains the post-trial diagnostic replay. Machine paths and raw execution logs
are excluded from the public package. All content is fictional.

```sh
python3 -B -m unittest discover -s tests -q
python3 -B scripts/evaluate_blind_context.py --compact
python3 -B scripts/score_context_packets.py \
  --packets examples/blind-evaluation/suite-a/improved-packets.json \
  --answers examples/blind-evaluation/suite-a/answers.json
```

At v0.4.1 the first command ran 98 automated tests; later versions add tests.
The second verifies frozen artifact hashes and the historical diagnostic patch.
From v0.5.0 it compares every current selected field with the sealed output by ID,
allowing new trace fields and ordering; it reports exact packet equality separately.
It is a replay, not another model evaluation. The third may exit nonzero for
anchor/label differences that reviewers waived; inspect the adjudication.

For another blind trial, use a new author and new raw documents; freeze answers,
hide them from the extractor, seal its output, then score and review. Reusing
these now-public answers as a supposed unseen benchmark would invalidate blinding.

Remaining limits: only two synthetic corpora, one run per version/corpus,
discretionary relevance judgments, possible author/scorer bias, no timing/cost
benchmark, no real Notion retrieval or writes. Prompt instructions and grounding
checks do not prove an arbitrary model interpretation correct or guarantee attack
resistance. No private workspace data or GitHub publishing was involved.

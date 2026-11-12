# Fictional Lantern Docs workspace

Everything in this directory was written as fiction. These are not exports,
anonymized customer records, or real Notion IDs. `demo://` links refer only to
entries in `snapshot.json` and are not fetchable web pages.

Lantern Docs is an imaginary document collaboration product. Its standard
workspace exports expire after 14 days. A proposed 60-day window appears in a
newer draft, while a seven-day policy is explicitly superseded. A cleanup task and
an exposure review depend on the accepted 14-day decision.

Expected review: find the 60-versus-14 potential conflict; cite D-014; show T-022
and the exposure review as impacts; do not treat D-060 as accepted or D-007 as
current. `edits.json` proposes adding review requirements to the draft, leaving
the policy unchanged until a replacement decision is actually approved.

## Shared project context for three tasks

`context-snapshot.json` extends the original snapshot with goals, fictional
interviews and competitors, requirements, design, tests, risks and open questions.
It keeps the original decision/impact evidence checks usable. Every added source
is fictional, including all customer interviews, competitor names and test results.

The requests in `requests/` all concern standard exports, using the same metadata
scope and budget. Korean request text is included for the host; the offline helper
uses explicit `type` and `topics`, so this does not measure language understanding.
`context-expectations.json` contains separate author-labeled relevance judgments;
the selector never reads that file.

Run `python3 -B scripts/evaluate_context.py --output-dir work/context-demo` from
the repository root. Inspect why the market packet selects interviews/competitors,
the design packet selects constraints and the known failure, and the QA packet
selects expected behavior and observed results. Follow the cleanup-risk citation
to see a dependency whose topic differs from the initial export query.

`context_prepared` means a context packet is assembled. In this fixture the QA
observation explicitly contains a failed expiry check; preparation is not a QA pass.

To try the agent offline, provide the snapshot and proposal and say:

> Use DecisionGuard to review the proposed 60-day export window using only these
> fictional pages. Explain current authority, impacts, and missing validation.
> Show a concrete change set. Do not write anything to Notion.

For a live connector smoke test, manually create equivalent pages in a disposable
Notion area, then ask for a review with that area's real root URL. Creating those
pages through an agent also requires confirmation. Do not paste real URLs back
into these public fixtures.

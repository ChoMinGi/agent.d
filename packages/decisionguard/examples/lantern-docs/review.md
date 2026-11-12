# Example review — fictional Lantern Docs

**Potential conflict in standard workspace export retention.** The proposed
60-day download window changes an accepted 14-day decision. This is a review of
the five supplied fictional pages, not an approval or a production risk assessment.

## Evidence and authority

- **Observed:** [D-014](demo://lantern-docs/policy) says “Standard workspace exports
  expire after 14 days” and explicitly records accepted status (fictional-r3).
- **Observed:** [D-060](demo://lantern-docs/experiment) proposes 60 days but is a
  draft (fictional-r9). Its later revision does not establish authority.
- **Observed:** [D-007](demo://lantern-docs/history) is explicitly superseded by
  D-014. The former seven-day value is historical context.
- **Potential conflict:** 60 days and 14 days cannot both be the standard expiry
  value. Replacing D-014 requires an explicit decision about the original rationale.

## Impact and missing validation

[T-022](demo://lantern-docs/tasks/cleanup) explicitly implements D-014, so an
accepted change would require its expiry behavior and acceptance checks to be
revisited. The [exposure review](demo://lantern-docs/evidence) says exported files
can contain private draft documents and calls for a new review when extending
the download window. A longer exposure window is a reasonable inference; the
fixture does not quantify its risk or prove users need 60 days.

Options: keep 14 days; investigate a narrower exception; or approve a replacement
decision after reviewing exposure, user need, cleanup behavior and expiry messaging.
None of those alternatives is already approved by the fixture.

## Concrete proposed change

Target: the draft experiment page, fictional-r9.

**Before:** “We have not reviewed the exposure impact.”

**After:** “Review required before acceptance: reassess download exposure, revise
D-014 if approved, and update T-022 plus expiry copy and tests.”

Rationale: record the prerequisites while retaining draft status. Evidence:
D-014, the exposure review, and T-022. This exact replacement is also available
in `edits.json` for the local planning command.

In a live run, the agent would now request confirmation of this edit, re-fetch
the target and evidence, apply only the confirmed text, and read it back. No live
Notion pages were read or changed to create this example.

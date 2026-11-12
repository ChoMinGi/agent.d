# ReadingLight research synthesis and prototype brief

The discovery supports a **staff-only prototype design for the two reading rooms at Bracken Civic Library**. It does not yet establish wider demand or a reduction in interruptions, and it does not authorize visitor-facing deployment.

## What we learned

- Researcher Mira Fen recorded six visitor interviews. Four interviewees said they abandoned a room after finding no seat. During two afternoon observations, observers counted nine unnecessary room entries. These are local reports and counts, not a population estimate or evidence that a seat map works. [Discovery, research paragraph, line 5](demo://readinglight/discovery)
- The stated purpose is to help visitors find space in the two reading rooms. Product steward **Sela Rowan accepted D-041 on 14 July 2027**: “prototype individual free/occupied seat dots, without visitor names, in these two rooms.” The notes expressly limit this to prototype design. [Discovery, decision paragraph, line 7](demo://readinglight/discovery)
- Librarian **Oren Vale’s** idea that a live seat map reduces interruptions across other branches remains **unverified**: “nobody has tested that market hypothesis.” Weekend and screen-reader users have not yet been interviewed. The source says this gap limits demand claims but does not prevent a staff-only prototype. [Discovery, research paragraph, line 5](demo://readinglight/discovery)

## What the team can design now

**Brief:** Design a staff-only prototype showing the two pilot rooms with individual seats in free/occupied states, without visitor names. Preserve D-041 as the accepted basis. Do not describe the prototype as a launched service. [Discovery, decision paragraph, line 7](demo://readinglight/discovery)

**Suggested design work, not additional accepted requirements:** sketch a two-room overview, seat-state dots and a clear legend; use sample occupancy data for a clickable walkthrough; include text labels alongside visual states so accessibility can be evaluated. Document navigation, state interpretation and questions that arise. The notes do not specify the data source, refresh behavior, error states or room layout, so treat those as design questions rather than settled requirements.

**Suggested evaluation:** use staff walkthroughs to check whether the representation communicates room and seat state. Plan interviews and usability sessions with weekend and screen-reader users before drawing conclusions about their needs. Keep any usability result distinct from proof of market demand or reduced interruptions. These are proposed next steps, not completed research or assigned commitments.

## What still needs validation

| Question or boundary | Action affected | Next useful check |
| --- | --- | --- |
| Missing weekend and screen-reader interviews | Claims about these users’ needs, accessibility and demand; does not prevent staff-only prototype design | Recruit those users and record findings separately from the current six interviews. |
| Untested cross-branch interruption hypothesis | Claims that a live map works or is needed across other branches | Study other branches and define an interruption measure and comparison before testing benefit. |
| Small local sample and no traffic denominator | Population prevalence, effect sizes or generalized demand | Preserve the counts as counts; collect observation duration, total entries and broader sampling before estimating rates. |
| Data supply and state behavior unspecified | A working live implementation | Clarify occupancy input, update behavior and failure handling; prototype assumptions can be explored without treating them as accepted decisions. |
| Separate release authority | Any visitor-facing deployment | Retrieve written release approval from **release chair Ivo Reed**, verify its exact scope, and check for later changes. No such approval is supplied here. |

The first three limits come from the [research paragraph](demo://readinglight/discovery). Implementation details are absent from this supplied note, so the fourth row is a proposed design check. The release boundary is explicit: “Any visitor-facing deployment requires a separate written release approval from release chair Ivo Reed.” [Discovery, decision paragraph, line 7](demo://readinglight/discovery)

## Proposed memory change — not approved

Target: the local ReadingLight handoff ledger. Before: no entries or receipts. Proposed after: add the following eight evidence-bound records, all scoped to `two-room-pilot`; exact normalized records and before/after bindings are in `snapshot.json` and the generated `plan.json`. All cite `discovery`, revision `r1`, with exact claim/status excerpts.

| Record | Proposed remembered content | Preserved kind/status |
| --- | --- | --- |
| G-001 | Stated purpose: help visitors find space in the two reading rooms; separate formal goal approval is not identified. | goal / unknown |
| CE-001 | Four of six interviewees reported abandoning a room after finding no seat; local self-reports. | customer_evidence / observed |
| CE-002 | Nine unnecessary room entries counted during two afternoon observations at this branch. | customer_evidence / observed |
| R-001 | These local observations do not establish demand for all library users. | risk / open |
| H-001 | Oren Vale’s cross-branch interruption-reduction hypothesis is untested. | assumption / unverified |
| Q-001 | Weekend and screen-reader users have not been interviewed; the gap limits demand claims without preventing a staff-only prototype. | question / open |
| D-041 | Sela Rowan accepted individual free/occupied seat dots, without visitor names, in these two rooms; prototype design only. | decision / accepted |
| REQ-RELEASE | Visitor-facing deployment requires separate written release approval from Ivo Reed; the supplied note does not establish that approval. | requirement / accepted |

Rationale: the next designer needs the observed problem, sample limits, untested benefit, current prototype choice and separate release authority together. Memory confirmation must preserve these states; it cannot validate the hypothesis or authorize implementation, release or wider sharing. The prototype suggestions above are not proposed as accepted memory.

Before reuse, re-read current discovery and any authoritative follow-ups; check whether D-041 or the release requirement changed, whether interviews or cross-branch studies answered the open questions, and whether a scoped written release approval actually exists. Keep a resolved research question separate from still-unknown execution or approval. No confirmation has been fabricated and no approved memory has been written.

## Provenance and coverage

Only the supplied **Reading room discovery notes**, dated 14 July 2027, were examined: source `discovery`, [demo://readinglight/discovery](demo://readinglight/discovery), revision `r1`, fictional fetch time `2027-07-14T10:01:00Z`; task as of `2027-07-14T10:02:00Z`. The entire raw document is preserved byte-for-byte in `source.md` and as source content in `snapshot.json`. Research and prototype context are prepared separately because the request mixes research synthesis and feature design. Coverage is limited to this source; no other author files, private material, example outputs or external services were consulted.

## Validation and observed limitations

The first extraction and normalized snapshot passed the helper checks; no validation repair was required. All eight proposed records are selected in both context packets, and the source content matches the raw file exactly. The helper marks context as needing more evidence: the goal is stated without separate formal approval, broader market evidence is absent, and the research/release evidence boundaries remain open. Its generic “later decision or authority requires follow-up” message does not mean a later decision was discovered. D-041 independently supplies the accepted authority for the scoped prototype design.

The empty ledger remains empty. `handoff.py plan` generated eight proposed additions only; no `confirm` operation was run. The exact plan is in `plan.json` and its readable rendering in `plan.md`; plan ID: `0ad274b98ed2ace95f55dda655c1c50cf8b924f706d6554811f350a02a177f34`. The first answer is preserved in `result.first.md`; this final copy adds validation observations without changing the synthesis or memory proposal.

# ReadingLight revised feature design and QA handoff

Use **D-052: one staff-selected availability band per room** for the two-room prototype. D-052 explicitly replaces D-041. The accepted design limits availability detail across **every display, stored record, and analytics event**, not just the visible interface. Nessa Clay’s later per-seat concept remains a discussion draft and is not a build requirement. This handoff authorizes no visitor-facing deployment. [Review, signed decision and later concept](demo://readinglight/review)

## Evidence and authority

This review checked only the complete supplied discovery and review documents, both revision `r1`, plus the inherited approved-memory ledger. “Approved memory” here means simulated fixture consent to remember the original evidence state; it does not make a claim true or authorize implementation or release.

| Source | Authority and exact anchor | Interpretation |
|---|---|---|
| [Discovery](demo://readinglight/discovery), lines 5 and 7 | “Four interviewees said they had abandoned a room after finding no seat”; product steward Sela Rowan accepted D-041 for prototype design only | Local problem evidence; historical seat-dot brief. |
| [Review](demo://readinglight/review), lines 3–5 | Signed by Sela Rowan: “I approve decision D-052, replacing D-041 for both pilot rooms.” | Explicit accepted successor for the same scope, not an inference from recency. |
| [Review](demo://readinglight/review), lines 7–9 | Nessa’s concept says “Sela has not reviewed or approved it.” | Draft per-seat map, exact vacancy count and automatic seat-level history cannot override D-052. No formal rejection is asserted. |
| [Discovery](demo://readinglight/discovery), line 7; [Review](demo://readinglight/review), line 5 | Separate written release approval from Ivo Reed is required; D-052 “does not authorize visitor deployment” | The release prerequisite remains current; no approval or deployment evidence is supplied. |

Source retrieval is the corrected fictional `2027-07-22T10:01:00Z`; task review is `2027-07-22T10:02:00Z`, with refresh starting `10:00:30Z`. The initial July 18 fixture clock preceded the July 19 and July 21 source dates. The coordinator corrected it after the inconsistency was reported. Raw source contents were preserved exactly, original timing inputs were saved separately, and no historical authority as of July 18 is claimed. See [timing correction](../timing-correction.md).

## Builder contract: accepted requirements

1. **Two room summaries.** Staff choose exactly one availability band for the room being updated: `none`, `a few`, or `several`. Represent the room, not individual seats. A simple card per room is the recommended presentation. D-052 covers both pilot rooms. [Review, line 5](demo://readinglight/review)
2. **Consistent granularity everywhere.** Availability detail is only the room identifier and band. Do not collect, transmit, store, display, or emit individual seat identifiers or exact seat counts as part of this feature. Apply this to visible UI, accessible text, hidden UI payloads, persisted records, caches and analytics. The latter implementation surfaces are derived enforcement points for the expressly stated display/storage/event rule. A hidden count or seat-level history is incompatible with that rule. [Review, line 5](demo://readinglight/review)
3. **Visible freshness.** Show the update time and mark information stale after ten minutes. Freshness metadata is distinct from availability detail: the same accepted paragraph expressly requires an update time. Do not infer seat occupancy or a vacancy count from the band. [Review, line 5](demo://readinglight/review)
4. **Prototype boundary.** Keep the work within prototype design. The supplied authority permits neither a visitor-facing rollout nor an assertion of release readiness. Obtain Ivo Reed’s separate scoped written approval before visitor deployment. [Discovery, line 7](demo://readinglight/discovery); [Review, line 5](demo://readinglight/review)

The reason for the granularity restriction is concrete: fine detail could let visitors infer where a person is sitting in these small rooms. Names alone were not the entire privacy concern. [Review, line 5](demo://readinglight/review)

## Proposed implementation details for builder review

These are recommended defaults derived from the accepted behavior; they are **not additional accepted decisions** and are not proposed for memory as established policy.

- **Staff flow:** select a pilot room, choose one of the three bands, then save. A successful save updates that room’s band and time together. Refreshing or reading a room must not reset its update time. A failed save leaves the last confirmed value/time intact and shows an error. Keep the two rooms independent.
- **Data shape:** use one latest-state record per room: `room_id`, `availability_band`, `updated_at`. Treat the room identifier as a configured pilot-room enum, band as the three-value enum, and update time as a timezone-aware server timestamp. Field names and timestamp origin are proposed. Validate allowed fields at input and persistence boundaries; reject seat identifiers and counts without copying rejected payloads into logs. Do not add numeric vacancy fields, per-seat arrays, positions, or seat-level history.
- **Analytics:** if an availability event is needed, its availability payload contains only room identifier and band. Any timestamp/event envelope must carry no additional occupancy detail. Check downstream enrichment and debug logging as well as the authored event schema; do not add analytics solely because the draft suggests history.
- **Stale behavior:** calculate age from the last successful update. Recommended boundary: stale when age is at least 600 seconds. Keep the last band visible with a clear “Stale” label and its actual update time; stale is a freshness state, not a fourth availability band. Re-saving a freshly observed band, including the same band, may refresh its time. Use text so neither availability nor freshness depends only on color.
- **No initial update:** show “No update yet”; do not default to `none`. No recorded band is not evidence of no availability. Connection failure likewise must not silently become `none` or look freshly updated.
- **No numeric thresholds:** the source calls for a staff choice and supplies no count-to-band boundaries. Keep manual selection; do not invent numeric thresholds or collect exact counts to derive the label. Qualitative staff guidance can be agreed separately.

Before final implementation acceptance, settle the exact equality boundary at ten minutes, timestamp/clock handling, concurrent update ordering and error/empty-state copy. If any earlier seat-detail implementation or stored records exist, inspect all data paths and agree an explicit transition/disposition before claiming D-052 compliance. No existing implementation or data was inspected, and no deletion is authorized by this handoff.

## What changed from the prototype brief

| Earlier brief or suggestion | Revised handling | Why |
|---|---|---|
| D-041 accepted individual free/occupied seat dots without names | D-041 is superseded; D-052 uses staff-selected room bands | Same product steward explicitly replaces D-041 for both rooms. |
| Earlier excerpt did not state the new cross-system granularity restriction | Apply band-and-room restriction to every display, stored record and analytics event; prohibit seat IDs and exact counts | D-052 explicitly broadens the requirement beyond what a screen shows. |
| No update-time/stale rule in the earlier brief | Show update time; mark stale after ten minutes | New accepted behavior in the signed review. |
| Nessa’s newer per-seat map, exact count and automatic seat history | Keep as unapproved draft; exclude those features from the build | Its author expressly says Sela has not reviewed or approved it; features conflict with D-052. |
| Prototype-only authority and separate release-chair approval | Retain unchanged | The review expressly keeps the deployment boundary. |

All before/after distinctions come from [discovery](demo://readinglight/discovery) and [review](demo://readinglight/review); no missing earlier brief has been reconstructed.

## Concise QA handoff

These are proposed checks, **not executed tests or passing results**. Bind the test run to the eventual build and record expected/actual outcomes.

| Check | Expected behavior and evidence to retain |
|---|---|
| Both rooms and all three bands | Exercise each band in each room. Updating one room does not change the other. Capture the displayed label and saved room/band. |
| Granularity across all destinations | Inspect UI including accessible/hidden content, network payloads, persisted records/caches, logs and analytics. No seat IDs, exact counts, per-seat maps or seat-level history. Attempt prohibited fields and verify rejection without logging their values. This tests the derived enforcement points of REQ-DATA-052. |
| Time and stale boundary | Verify actual update time is shown, unchanged by refresh. Test just before, at and just after ten minutes; at exactly ten minutes use the proposed `>= 600s` rule only after builder agreement. Capture clock and timestamp evidence. |
| Refresh after a staff update | A successful update, including confirmation of the same band, uses the agreed new time and clears stale status. A failed update leaves last confirmed information and freshness intact. These failure/confirmation mechanics are proposed defaults. |
| Missing data and presentation | No record shows “No update yet,” never fabricated `none`. Availability and stale status have text labels. This is a functional check, not proof that screen-reader users’ needs have been researched. |
| Authorization and release | Confirm the tested artifact remains within the prototype scope; separately inspect Ivo Reed’s written release approval before any visitor deployment. A completed build or passing tests do not substitute for that approval. |

## Reuse, changes and proposed memory delta

[Resume results](resume.json) report six selected inherited records as reusable: **CE-001, CE-002, G-001, Q-001, R-001 and REQ-RELEASE**. Their complete normalized records and discovery-source binding were preserved unchanged after rereading both documents. G-001 remains `unknown`, Q-001 remains `open`, and the local research limitation remains `open`; memory consent does not upgrade them. **H-001** is also preserved byte-for-value in the snapshot as `unverified`, but excluded from this task’s selected context because cross-branch demand is not needed for this prototype design.

Inherited follow-up prose is retained as historical provenance. In particular, G-001’s inherited rationale mentions D-041’s former authorization; the current authority is D-052 and the old decision is retired. The fresh review is recorded in [reuse audit](reuse-audit.json), not silently substituted into unchanged records.

The exact proposed memory change set is in [plan.json](plan.json), plan ID `88266370e7a07b411d4a44b86903cf491cf2f7e5c2f9799dd48883f0b7905030`:

| Record | Before | Proposed after |
|---|---|---|
| D-041 | Accepted seat-dot prototype choice | Same historical claim/value, now `superseded`, with review authority, explicit `superseded_by: D-052`, and changed follow-up evidence. |
| D-052 | Not in inherited memory | `accepted` room-band replacement; preserve prototype-only boundary and privacy rationale dependency. |
| REQ-DATA-052 | Not recorded | `accepted` granularity limits in displays, records and analytics. |
| REQ-FRESH-052 | Not recorded | `accepted` update-time and ten-minute stale requirement. |
| R-PRIVACY-052 | Not recorded | `open` privacy risk explaining the granularity limit; no claim of proven mitigation. |
| DESIGN-NESSA-01 | Not recorded | `draft` per-seat/count/history concept with explicit lack of approval and unresolved follow-up. |

No confirmation was fabricated, no confirmation command ran, and the inherited ledger was not mutated. The five new current records are source-supported context awaiting simulated memory consent; they are not yet approved memory. The coordinator can review and confirm this exact plan later under the existing fresh-read protocol.

## Deferred questions, blockers and validation limits

- **Deferred for this design:** weekend and screen-reader interviews remain missing. The signed review expressly says this coverage gap does not block design work. It does limit demand and accessibility claims; conduct those interviews before making such claims. Cross-branch benefit remains an untested hypothesis. [Discovery, line 5](demo://readinglight/discovery); [Review, line 5](demo://readinglight/review)
- **Deferred for drafting, needed for final implementation acceptance:** the proposed edge behaviors above need agreement and testing. Formal approval of the separate goal statement is not evidenced; if needed for governance, ask Sela for its authority. D-052 itself explicitly supplies the scoped design decision.
- **Blocks a compliance/pass claim:** no build, persisted data, event sample or test run was supplied. QA must execute the checks and inspect all destinations before asserting compliance; the design document alone is insufficient.
- **Blocks visitor deployment:** no separate written release approval from Ivo Reed is supplied. Source approval of the prototype, simulated memory consent and a successful helper check cannot replace it.

Raw extraction, normalized context validation, `handoff.py resume` and `handoff.py plan` all completed on their first validation attempts with exit code 0. First outputs are retained separately. The context result is **`needs_context`**, not release clearance: it retains unknown goal authority, missing execution evidence, the draft’s unresolved approval and implementation-detail gaps. There is no item-budget overflow, no accepted-decision conflict and no withheld memory. The helper’s generic “later decision or authority requires follow-up” wording on G-001 and the draft is an unresolved-state warning; it does not establish that another approved successor exists. Helpers check citation presence, states and bindings, not semantic truth. No external service, implementation or source write was performed.

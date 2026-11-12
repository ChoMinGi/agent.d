# Proposed memory change

Propose remembering only the new build 0.8 QA results, incomplete fix and accessibility execution, reported QA approval boundaries, release prerequisites, absent written release decision, and provisional opening. Preserve observed, planned, accepted, and open evidence states. Leave all inherited normalized records and the approved ledger unchanged. No consent, implementation, or release approval is supplied by this proposal.

Plan: d8c6c0af24bf08a732a9e451f177c4ab06615f0fcc8034aff9ca4f3fc7b1e1a0

These changes record context; they do not approve a policy or an external write.

## OPENING-MONDAY

Before: (not recorded)

After: {"id": "OPENING-MONDAY", "kind": "task", "title": "Front-desk Monday visitor opening is provisional", "scope": "two-room-pilot", "topics": ["release-readiness", "release-approval"], "status": "planned", "source_id": "qa", "quote": "The front desk's calendar entry “Monday visitor opening” is provisional.", "status_quote": "The front desk's calendar entry “Monday visitor opening” is provisional.", "attention": {"category": "approval_boundary", "quote": "The front desk's calendar entry “Monday visitor opening” is provisional.", "rationale": "Scheduling is provisional and is not evidence of release authorization."}}

Bound sources:
- demo://readinglight/qa @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [],
  "links": [],
  "sources": [
    {
      "id": "qa",
      "url": "demo://readinglight/qa",
      "revision": "r1",
      "source_sha256": "01103d5e136155b3ff3485080b26850d58cb35d9ad499946fd6e7cd5a2c270b3"
    }
  ]
}
```

## PATCH-Q13-08

Before: (not recorded)

After: {"id": "PATCH-Q13-08", "kind": "task", "title": "Pell Moss proposed a privacy patch; merge and retest remain outstanding", "scope": "two-room-pilot", "topics": ["data-minimization", "build-0.8", "release-readiness"], "status": "planned", "source_id": "qa", "quote": "Engineer Pell Moss has proposed a patch; it has not been merged or retested.", "status_quote": "Engineer Pell Moss has proposed a patch; it has not been merged or retested.", "attention": {"category": "missing_execution", "quote": "Engineer Pell Moss has proposed a patch; it has not been merged or retested.", "rationale": "A proposed fix is not an implemented fix or a passing privacy retest."}}

Bound sources:
- demo://readinglight/qa @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [
    {
      "id": "Q-13",
      "kind": "test_result",
      "title": "Build 0.8 privacy check failed: analytics emits seat identifiers and exact counts",
      "scope": "two-room-pilot",
      "topics": [
        "data-minimization",
        "build-0.8",
        "release-readiness"
      ],
      "status": "observed",
      "source_id": "qa",
      "quote": "Q-13 failed: the visible screen uses bands, but analytics still sends seat_id and exact_free_count from the earlier implementation.",
      "status_quote": "Q-13 failed: the visible screen uses bands, but analytics still sends seat_id and exact_free_count from the earlier implementation.",
      "attention": {
        "category": "known_failure",
        "quote": "Q-13 failed: the visible screen uses bands, but analytics still sends seat_id and exact_free_count from the earlier implementation.",
        "rationale": "The current analytics payload contradicts the accepted display/storage/analytics granularity requirement; passing screen checks do not remedy this failure."
      }
    }
  ],
  "links": [
    {
      "from_id": "PATCH-Q13-08",
      "to_id": "Q-13",
      "source_id": "qa",
      "quote": "Q-13 failed: the visible screen uses bands, but analytics still sends seat_id and exact_free_count from the earlier implementation. Engineer Pell Moss has proposed a patch; it has not been merged or retested."
    }
  ],
  "sources": [
    {
      "id": "qa",
      "url": "demo://readinglight/qa",
      "revision": "r1",
      "source_sha256": "01103d5e136155b3ff3485080b26850d58cb35d9ad499946fd6e7cd5a2c270b3"
    }
  ]
}
```

## Q-11

Before: (not recorded)

After: {"id": "Q-11", "kind": "test_result", "title": "Build 0.8: availability-band check passed in both rooms", "scope": "two-room-pilot", "topics": ["seat-availability", "build-0.8"], "status": "observed", "source_id": "qa", "quote": "Executed checks passed: Q-11 verified availability bands in both rooms;", "status_quote": "Executed checks passed: Q-11 verified availability bands in both rooms;"}

Bound sources:
- demo://readinglight/qa @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [],
  "links": [],
  "sources": [
    {
      "id": "qa",
      "url": "demo://readinglight/qa",
      "revision": "r1",
      "source_sha256": "01103d5e136155b3ff3485080b26850d58cb35d9ad499946fd6e7cd5a2c270b3"
    }
  ]
}
```

## Q-12

Before: (not recorded)

After: {"id": "Q-12", "kind": "test_result", "title": "Build 0.8: update-time and ten-minute stale-marker check passed", "scope": "two-room-pilot", "topics": ["seat-availability", "freshness", "build-0.8"], "status": "observed", "source_id": "qa", "quote": "Q-12 verified update times and the stale marker after ten minutes.", "status_quote": "Executed checks passed: Q-11 verified availability bands in both rooms; Q-12 verified update times and the stale marker after ten minutes."}

Bound sources:
- demo://readinglight/qa @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [],
  "links": [],
  "sources": [
    {
      "id": "qa",
      "url": "demo://readinglight/qa",
      "revision": "r1",
      "source_sha256": "01103d5e136155b3ff3485080b26850d58cb35d9ad499946fd6e7cd5a2c270b3"
    }
  ]
}
```

## Q-13

Before: (not recorded)

After: {"id": "Q-13", "kind": "test_result", "title": "Build 0.8 privacy check failed: analytics emits seat identifiers and exact counts", "scope": "two-room-pilot", "topics": ["data-minimization", "build-0.8", "release-readiness"], "status": "observed", "source_id": "qa", "quote": "Q-13 failed: the visible screen uses bands, but analytics still sends seat_id and exact_free_count from the earlier implementation.", "status_quote": "Q-13 failed: the visible screen uses bands, but analytics still sends seat_id and exact_free_count from the earlier implementation.", "attention": {"category": "known_failure", "quote": "Q-13 failed: the visible screen uses bands, but analytics still sends seat_id and exact_free_count from the earlier implementation.", "rationale": "The current analytics payload contradicts the accepted display/storage/analytics granularity requirement; passing screen checks do not remedy this failure."}}

Bound sources:
- demo://readinglight/qa @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [],
  "links": [],
  "sources": [
    {
      "id": "qa",
      "url": "demo://readinglight/qa",
      "revision": "r1",
      "source_sha256": "01103d5e136155b3ff3485080b26850d58cb35d9ad499946fd6e7cd5a2c270b3"
    }
  ]
}
```

## Q-14

Before: (not recorded)

After: {"id": "Q-14", "kind": "test_case", "title": "Q-14 screen-reader check is planned and unexecuted", "scope": "two-room-pilot", "topics": ["accessibility", "build-0.8", "release-readiness"], "status": "planned", "source_id": "qa", "quote": "Screen-reader check Q-14 remains unexecuted because the test device was unavailable.", "status_quote": "Screen-reader check Q-14 remains unexecuted because the test device was unavailable.", "attention": {"category": "missing_execution", "quote": "Screen-reader check Q-14 remains unexecuted because the test device was unavailable.", "rationale": "Visitor release needs an executed, passing screen-reader check; the device problem explains the missing run but does not waive it."}, "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "qa", "quote": "Screen-reader check Q-14 remains unexecuted because the test device was unavailable."}], "rationale": "Reviewed the full supplied QA report and its approval paragraph; no executed result or passing retest for Q-14 is supplied. QA-plan approval does not execute a test."}}

Bound sources:
- demo://readinglight/qa @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [],
  "links": [],
  "sources": [
    {
      "id": "qa",
      "url": "demo://readinglight/qa",
      "revision": "r1",
      "source_sha256": "01103d5e136155b3ff3485080b26850d58cb35d9ad499946fd6e7cd5a2c270b3"
    }
  ]
}
```

## Q-RELEASE-08

Before: (not recorded)

After: {"id": "Q-RELEASE-08", "kind": "question", "title": "Written release decision from sole release authority Ivo Reed remains absent", "scope": "two-room-pilot", "topics": ["release-approval", "release-readiness"], "status": "open", "source_id": "qa", "quote": "Ivo Reed, the sole release authority, has issued no written release decision.", "status_quote": "Ivo Reed, the sole release authority, has issued no written release decision.", "attention": {"category": "approval_boundary", "quote": "Ivo Reed, the sole release authority, has issued no written release decision.", "rationale": "Public opening remains unauthorized until the sole release authority issues a scoped written decision; a calendar entry cannot supply it."}, "followup": {"outcome": "unresolved", "evidence": [{"source_id": "qa", "quote": "Ivo Reed, the sole release authority, has issued no written release decision."}], "rationale": "The latest supplied report explicitly states that no written decision exists. Obtain Ivo’s scoped written release decision after passing required checks; no external search or release action was authorized for this review."}}

Bound sources:
- demo://readinglight/qa @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [],
  "links": [],
  "sources": [
    {
      "id": "qa",
      "url": "demo://readinglight/qa",
      "revision": "r1",
      "source_sha256": "01103d5e136155b3ff3485080b26850d58cb35d9ad499946fd6e7cd5a2c270b3"
    }
  ]
}
```

## REQ-APPROVAL-BOUNDARY-08

Before: (not recorded)

After: {"id": "REQ-APPROVAL-BOUNDARY-08", "kind": "requirement", "title": "Reported Sela approval covers prototype design and QA plan only", "scope": "two-room-pilot", "topics": ["prototype-scope", "release-approval"], "status": "accepted", "source_id": "qa", "quote": "Sela's email says, “Prototype design and the QA plan approved.” It does not approve deployment.", "status_quote": "Sela's email says, “Prototype design and the QA plan approved.” It does not approve deployment.", "attention": {"category": "approval_boundary", "quote": "Sela's email says, “Prototype design and the QA plan approved.” It does not approve deployment.", "rationale": "Do not interpret the product steward’s reported design/plan approval as visitor deployment approval."}, "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "qa", "quote": "Sela's email says, “Prototype design and the QA plan approved.” It does not approve deployment."}], "rationale": "Compared the reported email with the separate release requirement and explicit lack of Ivo’s decision. No deployment approval is established."}}

Bound sources:
- demo://readinglight/qa @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [],
  "links": [],
  "sources": [
    {
      "id": "qa",
      "url": "demo://readinglight/qa",
      "revision": "r1",
      "source_sha256": "01103d5e136155b3ff3485080b26850d58cb35d9ad499946fd6e7cd5a2c270b3"
    }
  ]
}
```

## REQ-RELEASE-TESTS-08

Before: (not recorded)

After: {"id": "REQ-RELEASE-TESTS-08", "kind": "requirement", "title": "Visitor release requires passing privacy and screen-reader checks", "scope": "two-room-pilot", "topics": ["release-readiness", "data-minimization", "accessibility"], "status": "accepted", "source_id": "qa", "quote": "Visitor release requires a passing privacy retest and an executed, passing screen-reader check.", "status_quote": "Sela's email says, “Prototype design and the QA plan approved.” It does not approve deployment.", "attention": {"category": "approval_boundary", "quote": "Visitor release requires a passing privacy retest and an executed, passing screen-reader check.", "rationale": "These QA prerequisites are necessary release evidence, not a substitute for Ivo Reed’s separate written release decision."}, "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "qa", "quote": "Visitor release requires a passing privacy retest and an executed, passing screen-reader check."}], "rationale": "The QA lead states the release test prerequisites and reports Sela’s approval of the QA plan in the same report. No later waiver or changed test gate appears in the supplied sources; the reported approval is limited to design and the QA plan."}}

Bound sources:
- demo://readinglight/qa @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [
    {
      "id": "Q-14",
      "kind": "test_case",
      "title": "Q-14 screen-reader check is planned and unexecuted",
      "scope": "two-room-pilot",
      "topics": [
        "accessibility",
        "build-0.8",
        "release-readiness"
      ],
      "status": "planned",
      "source_id": "qa",
      "quote": "Screen-reader check Q-14 remains unexecuted because the test device was unavailable.",
      "status_quote": "Screen-reader check Q-14 remains unexecuted because the test device was unavailable.",
      "attention": {
        "category": "missing_execution",
        "quote": "Screen-reader check Q-14 remains unexecuted because the test device was unavailable.",
        "rationale": "Visitor release needs an executed, passing screen-reader check; the device problem explains the missing run but does not waive it."
      },
      "followup": {
        "outcome": "no_change_found",
        "evidence": [
          {
            "source_id": "qa",
            "quote": "Screen-reader check Q-14 remains unexecuted because the test device was unavailable."
          }
        ],
        "rationale": "Reviewed the full supplied QA report and its approval paragraph; no executed result or passing retest for Q-14 is supplied. QA-plan approval does not execute a test."
      }
    }
  ],
  "links": [
    {
      "from_id": "REQ-RELEASE-TESTS-08",
      "to_id": "Q-14",
      "source_id": "qa",
      "quote": "Screen-reader check Q-14 remains unexecuted because the test device was unavailable. Visitor release requires a passing privacy retest and an executed, passing screen-reader check."
    }
  ],
  "sources": [
    {
      "id": "qa",
      "url": "demo://readinglight/qa",
      "revision": "r1",
      "source_sha256": "01103d5e136155b3ff3485080b26850d58cb35d9ad499946fd6e7cd5a2c270b3"
    }
  ]
}
```

## REQ-STAFF-TRIAL-08

Before: (not recorded)

After: {"id": "REQ-STAFF-TRIAL-08", "kind": "requirement", "title": "Current reported operating boundary permits supervised staff trials and excludes public opening", "scope": "two-room-pilot", "topics": ["prototype-scope", "release-approval"], "status": "accepted", "source_id": "qa", "quote": "Staff may continue supervised prototype trials; public opening is not authorized.", "status_quote": "Staff may continue supervised prototype trials; public opening is not authorized.", "attention": {"category": "approval_boundary", "quote": "Staff may continue supervised prototype trials; public opening is not authorized.", "rationale": "This is the operating boundary reported by the QA lead, consistent with prototype-only design approval. It grants no wider release authority."}, "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "qa", "quote": "Staff may continue supervised prototype trials; public opening is not authorized."}], "rationale": "The final supplied QA paragraph expressly retains supervised staff prototype trials and withholds public opening. This review repeats that reported boundary; it does not issue new permission."}}

Bound sources:
- demo://readinglight/qa @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [],
  "links": [],
  "sources": [
    {
      "id": "qa",
      "url": "demo://readinglight/qa",
      "revision": "r1",
      "source_sha256": "01103d5e136155b3ff3485080b26850d58cb35d9ad499946fd6e7cd5a2c270b3"
    }
  ]
}
```

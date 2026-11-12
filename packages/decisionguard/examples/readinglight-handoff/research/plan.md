# Proposed memory change

Propose remembering the ReadingLight discovery evidence, limits, D-041 prototype choice and separate visitor-facing release prerequisite; preserve every evidence state. No memory approval or execution authority is implied.

Plan: 0ad274b98ed2ace95f55dda655c1c50cf8b924f706d6554811f350a02a177f34

These changes record context; they do not approve a policy or an external write.

## CE-001

Before: (not recorded)

After: {"id": "CE-001", "scope": "two-room-pilot", "topics": ["seat-availability", "local-discovery"], "status": "observed", "source_id": "discovery", "quote": "Researcher Mira Fen recorded six visitor interviews and two afternoon observations at this branch. Four interviewees said they had abandoned a room after finding no seat;", "status_quote": "Researcher Mira Fen recorded six visitor interviews and two afternoon observations at this branch.", "kind": "customer_evidence", "title": "Four of six interviewees reported abandoning a room after finding no seat"}

Bound sources:
- demo://readinglight/discovery @ r1

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
      "id": "discovery",
      "url": "demo://readinglight/discovery",
      "revision": "r1",
      "source_sha256": "396de7bceed88690a7eea8344e56ca0b80783833092a2efa2b19b9fa1ef92cf4"
    }
  ]
}
```

## CE-002

Before: (not recorded)

After: {"id": "CE-002", "scope": "two-room-pilot", "topics": ["seat-availability", "local-discovery"], "status": "observed", "source_id": "discovery", "quote": "Researcher Mira Fen recorded six visitor interviews and two afternoon observations at this branch. Four interviewees said they had abandoned a room after finding no seat; observers counted nine unnecessary room entries.", "status_quote": "observers counted nine unnecessary room entries.", "kind": "customer_evidence", "title": "Nine unnecessary room entries counted during two afternoon observations"}

Bound sources:
- demo://readinglight/discovery @ r1

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
      "id": "discovery",
      "url": "demo://readinglight/discovery",
      "revision": "r1",
      "source_sha256": "396de7bceed88690a7eea8344e56ca0b80783833092a2efa2b19b9fa1ef92cf4"
    }
  ]
}
```

## D-041

Before: (not recorded)

After: {"id": "D-041", "scope": "two-room-pilot", "topics": ["seat-availability", "prototype-scope"], "status": "accepted", "source_id": "discovery", "quote": "Product steward Sela Rowan accepted decision D-041 today: prototype individual free/occupied seat dots, without visitor names, in these two rooms. This authorizes prototype design only.", "status_quote": "Product steward Sela Rowan accepted decision D-041 today:", "attention": {"category": "approval_boundary", "rationale": "Acceptance permits the prototype design and does not authorize visitor-facing deployment.", "quote": "This authorizes prototype design only."}, "key": "prototype-seat-representation", "value": "Individual free/occupied seat dots without visitor names in the two pilot rooms; prototype design only.", "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "discovery", "quote": "Product steward Sela Rowan accepted decision D-041 today: prototype individual free/occupied seat dots, without visitor names, in these two rooms. This authorizes prototype design only."}, {"source_id": "discovery", "quote": "Any visitor-facing deployment requires a separate written release approval from release chair Ivo Reed."}], "rationale": "Checked the complete supplied note for an amended or superseding prototype choice; none is present. Acceptance remains limited to design. Re-fetch D-041 and any later authoritative changes before reuse; this is not an exhaustive workspace check."}, "kind": "decision", "title": "Reading room discovery notes"}

Bound sources:
- demo://readinglight/discovery @ r1

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
      "id": "discovery",
      "url": "demo://readinglight/discovery",
      "revision": "r1",
      "source_sha256": "396de7bceed88690a7eea8344e56ca0b80783833092a2efa2b19b9fa1ef92cf4"
    }
  ]
}
```

## G-001

Before: (not recorded)

After: {"id": "G-001", "scope": "two-room-pilot", "topics": ["seat-availability"], "status": "unknown", "source_id": "discovery", "quote": "ReadingLight will help visitors find space in the library's two reading rooms.", "status_quote": "ReadingLight will help visitors find space in the library's two reading rooms.", "kind": "goal", "title": "Stated purpose: help visitors find space in two reading rooms", "followup": {"outcome": "unresolved", "evidence": [{"source_id": "discovery", "quote": "ReadingLight will help visitors find space in the library's two reading rooms."}], "rationale": "Checked all four passages of discovery r1. The purpose is stated but separate goal-approval authority is not identified. If formal goal approval matters, ask the product steward for the applicable decision; D-041 independently authorizes the scoped prototype design."}}

Bound sources:
- demo://readinglight/discovery @ r1

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
      "id": "discovery",
      "url": "demo://readinglight/discovery",
      "revision": "r1",
      "source_sha256": "396de7bceed88690a7eea8344e56ca0b80783833092a2efa2b19b9fa1ef92cf4"
    }
  ]
}
```

## H-001

Before: (not recorded)

After: {"id": "H-001", "scope": "two-room-pilot", "topics": ["cross-branch-demand", "seat-availability"], "status": "unverified", "source_id": "discovery", "quote": "Librarian Oren Vale suspects that a live seat map would reduce interruptions across other branches; nobody has tested that market hypothesis.", "status_quote": "nobody has tested that market hypothesis.", "kind": "assumption", "title": "Oren Vale hypothesizes that a live seat map reduces interruptions across other branches"}

Bound sources:
- demo://readinglight/discovery @ r1

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
      "id": "discovery",
      "url": "demo://readinglight/discovery",
      "revision": "r1",
      "source_sha256": "396de7bceed88690a7eea8344e56ca0b80783833092a2efa2b19b9fa1ef92cf4"
    }
  ]
}
```

## Q-001

Before: (not recorded)

After: {"id": "Q-001", "scope": "two-room-pilot", "topics": ["research-generalization", "accessibility"], "status": "open", "source_id": "discovery", "quote": "Weekend and screen-reader users have not yet been interviewed. That gap limits demand claims but does not prevent a staff-only prototype.", "status_quote": "Weekend and screen-reader users have not yet been interviewed.", "kind": "question", "title": "Weekend and screen-reader user needs remain unresearched", "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "discovery", "quote": "Weekend and screen-reader users have not yet been interviewed. That gap limits demand claims but does not prevent a staff-only prototype."}], "rationale": "Checked the full supplied discovery note for later answers; none resolves these missing interviews. No follow-up document is linked. Preserve the open research need and check newer interviews before making demand or accessibility claims."}}

Bound sources:
- demo://readinglight/discovery @ r1

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
      "id": "discovery",
      "url": "demo://readinglight/discovery",
      "revision": "r1",
      "source_sha256": "396de7bceed88690a7eea8344e56ca0b80783833092a2efa2b19b9fa1ef92cf4"
    }
  ]
}
```

## R-001

Before: (not recorded)

After: {"id": "R-001", "scope": "two-room-pilot", "topics": ["research-generalization"], "status": "open", "source_id": "discovery", "quote": "These are local observations, not evidence about all library users.", "status_quote": "These are local observations, not evidence about all library users.", "kind": "risk", "title": "Local discovery cannot establish demand for all library users"}

Bound sources:
- demo://readinglight/discovery @ r1

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
      "id": "discovery",
      "url": "demo://readinglight/discovery",
      "revision": "r1",
      "source_sha256": "396de7bceed88690a7eea8344e56ca0b80783833092a2efa2b19b9fa1ef92cf4"
    }
  ]
}
```

## REQ-RELEASE

Before: (not recorded)

After: {"id": "REQ-RELEASE", "scope": "two-room-pilot", "topics": ["release-approval", "prototype-scope"], "status": "accepted", "source_id": "discovery", "quote": "Any visitor-facing deployment requires a separate written release approval from release chair Ivo Reed.", "status_quote": "Product steward Sela Rowan accepted decision D-041 today: prototype individual free/occupied seat dots, without visitor names, in these two rooms. This authorizes prototype design only. Any visitor-facing deployment requires a separate written release approval from release chair Ivo Reed.", "attention": {"category": "approval_boundary", "rationale": "Before visitor-facing deployment, retrieve the specific written release approval and verify its scope; this source supplies the requirement, not the approval.", "quote": "Any visitor-facing deployment requires a separate written release approval from release chair Ivo Reed."}, "kind": "requirement", "title": "Visitor-facing deployment requires separate written approval from release chair Ivo Reed", "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "discovery", "quote": "Any visitor-facing deployment requires a separate written release approval from release chair Ivo Reed."}], "rationale": "The supplied note retains the separate written-release requirement and contains no written release approval. The requirement is current in this source; actual release approval and deployment are not established. Retrieve Ivo Reed’s scoped written approval before any visitor-facing deployment."}}

Bound sources:
- demo://readinglight/discovery @ r1

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
      "id": "discovery",
      "url": "demo://readinglight/discovery",
      "revision": "r1",
      "source_sha256": "396de7bceed88690a7eea8344e56ca0b80783833092a2efa2b19b9fa1ef92cf4"
    }
  ]
}
```

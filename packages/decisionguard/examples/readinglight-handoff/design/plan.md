# Proposed memory change

Remember only the reviewed delta: retire D-041 in favor of accepted D-052; preserve D-052’s prototype-only authority, display/storage/analytics granularity and freshness requirements; retain the privacy rationale and unapproved concept as an open risk and draft. Unchanged inherited records remain intact. This proposal is not memory consent or deployment approval.

Plan: 88266370e7a07b411d4a44b86903cf491cf2f7e5c2f9799dd48883f0b7905030

These changes record context; they do not approve a policy or an external write.

## D-041

Before: {"id": "D-041", "scope": "two-room-pilot", "topics": ["seat-availability", "prototype-scope"], "status": "accepted", "source_id": "discovery", "quote": "Product steward Sela Rowan accepted decision D-041 today: prototype individual free/occupied seat dots, without visitor names, in these two rooms. This authorizes prototype design only.", "status_quote": "Product steward Sela Rowan accepted decision D-041 today:", "attention": {"category": "approval_boundary", "rationale": "Acceptance permits the prototype design and does not authorize visitor-facing deployment.", "quote": "This authorizes prototype design only."}, "key": "prototype-seat-representation", "value": "Individual free/occupied seat dots without visitor names in the two pilot rooms; prototype design only.", "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "discovery", "quote": "Product steward Sela Rowan accepted decision D-041 today: prototype individual free/occupied seat dots, without visitor names, in these two rooms. This authorizes prototype design only."}, {"source_id": "discovery", "quote": "Any visitor-facing deployment requires a separate written release approval from release chair Ivo Reed."}], "rationale": "Checked the complete supplied note for an amended or superseding prototype choice; none is present. Acceptance remains limited to design. Re-fetch D-041 and any later authoritative changes before reuse; this is not an exhaustive workspace check."}, "kind": "decision", "title": "Reading room discovery notes"}

After: {"id": "D-041", "scope": "two-room-pilot", "topics": ["seat-availability", "prototype-scope"], "status": "superseded", "source_id": "discovery", "quote": "Product steward Sela Rowan accepted decision D-041 today: prototype individual free/occupied seat dots, without visitor names, in these two rooms. This authorizes prototype design only.", "status_quote": "I approve decision D-052, replacing D-041 for both pilot rooms.", "status_source_id": "review", "attention": {"category": "approval_boundary", "rationale": "Acceptance permits the prototype design and does not authorize visitor-facing deployment.", "quote": "This authorizes prototype design only."}, "key": "prototype-seat-representation", "value": "Individual free/occupied seat dots without visitor names in the two pilot rooms; prototype design only.", "superseded_by": "D-052", "followup": {"outcome": "changed", "evidence": [{"source_id": "review", "quote": "I approve decision D-052, replacing D-041 for both pilot rooms."}], "rationale": "Signed product-steward review explicitly replaces D-041 with D-052 for both rooms. Checked the later Nessa concept: it expressly lacks review and approval, so it does not change this successor. Visitor deployment remains unauthorized.", "successor_id": "D-052"}, "kind": "decision", "title": "Reading room discovery notes"}

Bound sources:
- demo://readinglight/discovery @ r1
- demo://readinglight/review @ r1

Before bindings (dependencies, relationships and source fingerprints):

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

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [
    {
      "id": "D-052",
      "scope": "two-room-pilot",
      "topics": [
        "seat-availability",
        "prototype-scope"
      ],
      "status": "accepted",
      "source_id": "review",
      "quote": "I approve decision D-052, replacing D-041 for both pilot rooms. Staff will choose one availability band: “none,” “a few,” or “several.”",
      "status_quote": "I approve decision D-052, replacing D-041 for both pilot rooms.",
      "attention": {
        "category": "approval_boundary",
        "rationale": "The approved replacement governs prototype design; it explicitly does not authorize visitor deployment.",
        "quote": "This is the accepted prototype design; it does not authorize visitor deployment."
      },
      "key": "prototype-seat-representation",
      "value": "Staff choose one room-level availability band: none, a few, or several, for both pilot rooms; prototype design only.",
      "followup": {
        "outcome": "no_change_found",
        "evidence": [
          {
            "source_id": "review",
            "quote": "I approve decision D-052, replacing D-041 for both pilot rooms."
          },
          {
            "source_id": "review",
            "quote": "Sela has not reviewed or approved it. Please treat this as a discussion draft for next week's workshop."
          }
        ],
        "rationale": "Checked the signed review and the later circulated concept in the complete supplied review r1. The later concept expressly lacks Sela’s approval; it does not supersede the accepted D-052 prototype requirements. No other follow-up source is supplied."
      },
      "kind": "decision",
      "title": "Prototype review and design correspondence"
    },
    {
      "id": "R-PRIVACY-052",
      "scope": "two-room-pilot",
      "topics": [
        "seat-availability",
        "data-minimization"
      ],
      "status": "open",
      "source_id": "review",
      "quote": "Visitors could otherwise infer where a person is sitting in our small rooms.",
      "status_quote": "Visitors could otherwise infer where a person is sitting in our small rooms.",
      "kind": "risk",
      "title": "Fine-grained availability can reveal where an individual is sitting"
    }
  ],
  "links": [
    {
      "from_id": "D-052",
      "to_id": "R-PRIVACY-052",
      "source_id": "review",
      "quote": "Availability detail in every display, stored record, and analytics event is limited to the band and room identifier; individual seat identifiers and exact seat counts are prohibited. Visitors could otherwise infer where a person is sitting in our small rooms."
    }
  ],
  "sources": [
    {
      "id": "discovery",
      "url": "demo://readinglight/discovery",
      "revision": "r1",
      "source_sha256": "396de7bceed88690a7eea8344e56ca0b80783833092a2efa2b19b9fa1ef92cf4"
    },
    {
      "id": "review",
      "url": "demo://readinglight/review",
      "revision": "r1",
      "source_sha256": "fee4fa9cfe10138c8512457fae2bc00b446e017818bed2a0d82c8a0ac6ce9363"
    }
  ]
}
```

## D-052

Before: (not recorded)

After: {"id": "D-052", "scope": "two-room-pilot", "topics": ["seat-availability", "prototype-scope"], "status": "accepted", "source_id": "review", "quote": "I approve decision D-052, replacing D-041 for both pilot rooms. Staff will choose one availability band: “none,” “a few,” or “several.”", "status_quote": "I approve decision D-052, replacing D-041 for both pilot rooms.", "attention": {"category": "approval_boundary", "rationale": "The approved replacement governs prototype design; it explicitly does not authorize visitor deployment.", "quote": "This is the accepted prototype design; it does not authorize visitor deployment."}, "key": "prototype-seat-representation", "value": "Staff choose one room-level availability band: none, a few, or several, for both pilot rooms; prototype design only.", "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "review", "quote": "I approve decision D-052, replacing D-041 for both pilot rooms."}, {"source_id": "review", "quote": "Sela has not reviewed or approved it. Please treat this as a discussion draft for next week's workshop."}], "rationale": "Checked the signed review and the later circulated concept in the complete supplied review r1. The later concept expressly lacks Sela’s approval; it does not supersede the accepted D-052 prototype requirements. No other follow-up source is supplied."}, "kind": "decision", "title": "Prototype review and design correspondence"}

Bound sources:
- demo://readinglight/review @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [
    {
      "id": "R-PRIVACY-052",
      "scope": "two-room-pilot",
      "topics": [
        "seat-availability",
        "data-minimization"
      ],
      "status": "open",
      "source_id": "review",
      "quote": "Visitors could otherwise infer where a person is sitting in our small rooms.",
      "status_quote": "Visitors could otherwise infer where a person is sitting in our small rooms.",
      "kind": "risk",
      "title": "Fine-grained availability can reveal where an individual is sitting"
    }
  ],
  "links": [
    {
      "from_id": "D-052",
      "to_id": "R-PRIVACY-052",
      "source_id": "review",
      "quote": "Availability detail in every display, stored record, and analytics event is limited to the band and room identifier; individual seat identifiers and exact seat counts are prohibited. Visitors could otherwise infer where a person is sitting in our small rooms."
    }
  ],
  "sources": [
    {
      "id": "review",
      "url": "demo://readinglight/review",
      "revision": "r1",
      "source_sha256": "fee4fa9cfe10138c8512457fae2bc00b446e017818bed2a0d82c8a0ac6ce9363"
    }
  ]
}
```

## DESIGN-NESSA-01

Before: (not recorded)

After: {"id": "DESIGN-NESSA-01", "scope": "two-room-pilot", "topics": ["seat-availability", "data-minimization"], "status": "draft", "source_id": "review", "quote": "My revised concept offers a much clearer per-seat map, exact vacancy count, and automatic seat-level history.", "status_quote": "Sela has not reviewed or approved it. Please treat this as a discussion draft for next week's workshop.", "kind": "design", "title": "Unapproved concept: per-seat map, exact count and seat-level history", "followup": {"outcome": "unresolved", "evidence": [{"source_id": "review", "quote": "Sela has not reviewed or approved it. Please treat this as a discussion draft for next week's workshop."}, {"source_id": "review", "quote": "Availability detail in every display, stored record, and analytics event is limited to the band and room identifier; individual seat identifiers and exact seat counts are prohibited."}], "rationale": "The source explicitly withholds approval and proposes features incompatible with D-052. Do not implement it under D-052; a scoped authoritative replacement would be needed before these features could become requirements."}}

Bound sources:
- demo://readinglight/review @ r1

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
      "id": "review",
      "url": "demo://readinglight/review",
      "revision": "r1",
      "source_sha256": "fee4fa9cfe10138c8512457fae2bc00b446e017818bed2a0d82c8a0ac6ce9363"
    }
  ]
}
```

## R-PRIVACY-052

Before: (not recorded)

After: {"id": "R-PRIVACY-052", "scope": "two-room-pilot", "topics": ["seat-availability", "data-minimization"], "status": "open", "source_id": "review", "quote": "Visitors could otherwise infer where a person is sitting in our small rooms.", "status_quote": "Visitors could otherwise infer where a person is sitting in our small rooms.", "kind": "risk", "title": "Fine-grained availability can reveal where an individual is sitting"}

Bound sources:
- demo://readinglight/review @ r1

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
      "id": "review",
      "url": "demo://readinglight/review",
      "revision": "r1",
      "source_sha256": "fee4fa9cfe10138c8512457fae2bc00b446e017818bed2a0d82c8a0ac6ce9363"
    }
  ]
}
```

## REQ-DATA-052

Before: (not recorded)

After: {"id": "REQ-DATA-052", "scope": "two-room-pilot", "topics": ["seat-availability", "data-minimization"], "status": "accepted", "source_id": "review", "quote": "Availability detail in every display, stored record, and analytics event is limited to the band and room identifier; individual seat identifiers and exact seat counts are prohibited.", "status_quote": "This is the accepted prototype design; it does not authorize visitor deployment.", "kind": "requirement", "title": "Availability granularity is restricted in displays, records and analytics", "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "review", "quote": "I approve decision D-052, replacing D-041 for both pilot rooms."}, {"source_id": "review", "quote": "Sela has not reviewed or approved it. Please treat this as a discussion draft for next week's workshop."}], "rationale": "Checked the signed review and the later circulated concept in the complete supplied review r1. The later concept expressly lacks Sela’s approval; it does not supersede the accepted D-052 prototype requirements. No other follow-up source is supplied."}}

Bound sources:
- demo://readinglight/review @ r1

Before bindings (dependencies, relationships and source fingerprints):

```json
null
```

After bindings (dependencies, relationships and source fingerprints):

```json
{
  "dependencies": [
    {
      "id": "R-PRIVACY-052",
      "scope": "two-room-pilot",
      "topics": [
        "seat-availability",
        "data-minimization"
      ],
      "status": "open",
      "source_id": "review",
      "quote": "Visitors could otherwise infer where a person is sitting in our small rooms.",
      "status_quote": "Visitors could otherwise infer where a person is sitting in our small rooms.",
      "kind": "risk",
      "title": "Fine-grained availability can reveal where an individual is sitting"
    }
  ],
  "links": [
    {
      "from_id": "REQ-DATA-052",
      "to_id": "R-PRIVACY-052",
      "source_id": "review",
      "quote": "Availability detail in every display, stored record, and analytics event is limited to the band and room identifier; individual seat identifiers and exact seat counts are prohibited. Visitors could otherwise infer where a person is sitting in our small rooms."
    }
  ],
  "sources": [
    {
      "id": "review",
      "url": "demo://readinglight/review",
      "revision": "r1",
      "source_sha256": "fee4fa9cfe10138c8512457fae2bc00b446e017818bed2a0d82c8a0ac6ce9363"
    }
  ]
}
```

## REQ-FRESH-052

Before: (not recorded)

After: {"id": "REQ-FRESH-052", "scope": "two-room-pilot", "topics": ["seat-availability", "freshness"], "status": "accepted", "source_id": "review", "quote": "Show an update time and mark information stale after ten minutes.", "status_quote": "This is the accepted prototype design; it does not authorize visitor deployment.", "kind": "requirement", "title": "Display update time and stale status after ten minutes", "followup": {"outcome": "no_change_found", "evidence": [{"source_id": "review", "quote": "I approve decision D-052, replacing D-041 for both pilot rooms."}, {"source_id": "review", "quote": "Sela has not reviewed or approved it. Please treat this as a discussion draft for next week's workshop."}], "rationale": "Checked the signed review and the later circulated concept in the complete supplied review r1. The later concept expressly lacks Sela’s approval; it does not supersede the accepted D-052 prototype requirements. No other follow-up source is supplied."}}

Bound sources:
- demo://readinglight/review @ r1

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
      "id": "review",
      "url": "demo://readinglight/review",
      "revision": "r1",
      "source_sha256": "fee4fa9cfe10138c8512457fae2bc00b446e017818bed2a0d82c8a0ac6ce9363"
    }
  ]
}
```

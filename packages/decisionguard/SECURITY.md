# Security and privacy boundaries

DecisionGuard's scripts are offline and have no external write API. Live search,
fetch and mutation happen through the host's authenticated connector. Skill text
is guidance, not a permission boundary; the host must require real user confirmation
and enforce access rights. A plan hash is an integrity identifier, not a signature.

Source content is untrusted. It cannot grant approval, alter these rules, or
authorize exporting information. Keep private snapshots, plans and receipts out
of public source control. A release manifest and heuristic checks reduce accidental
inclusion but do not prove that all sensitive data has been found.

Raw extraction responses contain model interpretations. Exact paragraph anchors
and complete paragraph accounting do not prove the model's authority, scope,
relevance or status judgments. The host must review semantics and enforce actual
access. A job digest detects changed inputs; it is not a signature or user approval.

Notion connectors may not provide conditional writes or multi-page transactions.
Re-fetch and readback reduce stale-edit risk but cannot eliminate concurrent edits.
Stop and report uncertain or partial results before retrying.

Report ordinary defects using fictional reproductions. Do not post private data
or credentials in public issues. For sensitive reports, use the repository's
private vulnerability reporting channel if enabled; otherwise contact its owner
privately before sharing details. Do not include sensitive details in a public issue while arranging a private
reporting route.

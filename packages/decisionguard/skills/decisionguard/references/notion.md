# Notion adapter

This is a capability contract, not a bundled Notion client. Use the connector
already authenticated in the host. No API key, server, or vector database is
required by DecisionGuard itself. Without a connector, use supplied exports or
the fictional demo and state that live workspace coverage is unverified.

| Capability | Use | Incomplete/error behavior |
| --- | --- | --- |
| Search pages/data sources | Find scope, synonyms, decisions and dependents | Record query, filters and limits; zero results does not prove absence |
| Fetch page and metadata | Read actual text, status, URL, edit revision and relations | Inspect truncation, unknown blocks and permissions; fetch relevant children when available |
| Inspect/query database schema | Understand native fields and related records | Keep the existing schema; do not fabricate field names |
| Fetch linked evidence | Validate rationale, exceptions, and supersession | Only within authorized scope; mark inaccessible evidence |
| Update/create and read back | Apply a confirmed, precise change | Follow the commit protocol; no write access means return a manual patch |

Discover actual tools before calling them. Hosts may expose names such as
`search`, `fetch`, `notion-search`, or `notion-fetch`; argument schemas differ.
Use a supplied page/root or data source filter where supported. Follow available
pagination cursors; if pagination or full-text coverage is unavailable, disclose
that limit. Do not describe title-only search as a complete content search.

For pages returned as Markdown, retain stable page/block URLs. For a raw API
adapter, page properties alone are not the body: retrieve relevant block children
and nested children as well. Do not treat a signed attachment URL as a permanent
source identifier. Read the connector's current formatting specification before
editing complex blocks, tables, or properties.

Bootstrap output can stay in chat: scope/root, the discovered policy and decision
locations, their authority/status conventions, important evidence and task links,
and gaps. Persisting that map back to Notion is a separate confirmed change.

## Local normalization

Before carrying an old "undecided", "next question", or approved behavior into a
new task, search its decision/issue ID, subject and synonyms in the native decision
register and linked follow-ups. Read the actual later answer, its approval and
scope. A link to a plan is not a run result. Counts from an earlier subset are not
necessarily contradictory to a later complete register.

Record the query scope/limits privately and the cited outcome: no change found
in checked sources, a grounded change, or unresolved authority. In structured
extraction mode, encode this in v2 `followup_reviews`; direct reading does not
require the JSON artifact. Check both the earlier claim and the proposed successor.
When only one clause was answered, split it from remaining implementation,
measurement and approval questions. An inaccessible referenced follow-up remains
an explicit gap. Do not mark the whole page superseded because one issue changed,
or mark a later draft accepted because its date is newer. Stop discovery when the
material questions have cited dispositions or explicit retrieval gaps; do not
search unrelated workspaces to claim completeness.

For pipe tables preserve column headings, row text, source lines and qualifications
when exporting. Never concatenate a customer observation, buying intention and
approved behavior into one evidence record. HTML tables or merged cells require
host normalization with original anchors; the helper only splits ordinary
Markdown pipe tables.

A fetched page with a paragraph “Accepted: exports expire after 14 days” can become
a claim with `key=export.retention_days`, `scope=standard`, `value="14"`, and exact
`quote` / `status_quote` evidence. This is a local review representation, not a
required Notion property layout. A task asking to extend retention is an impact or
proposal, not an accepted policy. Check exceptions before normalizing the scope.

Keep private snapshots outside the repository during local use.
Public fixtures must be authored as fiction, not lightly anonymized
exports. The release packager uses an explicit file list.

## Official references

- [Notion MCP](https://developers.notion.com/guides/mcp/mcp): connection options.
- [Notion MCP security](https://developers.notion.com/guides/mcp/mcp-security-best-practices): untrusted tool content and confirmation before changes.
- [Retrieve block children](https://developers.notion.com/reference/get-block-children): raw API adapters.

Live connector behavior varies. This release was validated offline; a live read,
confirmed write, and readback in a disposable workspace remain a separate test.

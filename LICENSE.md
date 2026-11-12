# Licensing and external components

The repository-level [MIT license](LICENSE) covers the root documentation, catalog and integration scripts authored for agent.d.

- [Cognitive Partner](packages/cognitive-partner/LICENSE): MIT, selected by the owner for publication in agent.d.
- [DecisionGuard](packages/decisionguard/LICENSE): MIT, with its original copyright notice retained.
- [Web Feature Demo](packages/web-feature-demo/LICENSE): MIT, with its original copyright notice retained.

Keep each package's LICENSE with its independent installation or archive. The source snapshots and publication edits are recorded separately in `catalog.json`; the license change does not rewrite the original repository or its historical notice.

## External components

No dependency, credential, browser binary, or original repository Git history is vendored here. Cognitive Partner's development validator depends on PyYAML, installed separately. Web Feature Demo can install playwright-core and FFmpeg through its existing installer and uses an independently installed Chrome. Their own licenses and notices still apply. Review those terms before redistributing dependency or browser binaries.

Example apps, screenshots, videos and fictional evaluation fixtures retain their source provenance. MIT notices from the original packages remain included. Content review and source traceability help detect problems but are not an independent legal ownership audit.

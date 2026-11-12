# Package-specific licensing

There is no blanket license for this monorepo.

- `packages/cognitive-partner/`: [license selection pending](packages/cognitive-partner/LICENSE). Its existing notice grants no reuse or redistribution rights. Public visibility alone is not an open-source license.
- `packages/decisionguard/`: [MIT](packages/decisionguard/LICENSE), with the original copyright notice retained.
- `packages/web-feature-demo/`: [MIT](packages/web-feature-demo/LICENSE), with the original copyright notice retained.

Root documentation, catalog and integration scripts do not receive a new license through this migration. The owner has not selected one. Package licenses do not silently extend to the whole tree.

The individual installation and packaging tools retain each package's LICENSE. They do not grant rights beyond those notices. Owner-local preparation and installation checks are not a public distribution grant.

## External components

No third-party dependency, credential, browser binary, or original Git history is vendored here. Cognitive Partner's development validator depends on PyYAML (installed separately). Web Feature Demo can install playwright-core and FFmpeg through its existing installer, and uses an independently installed Chrome. Their own licenses and notices still apply. Inspect them before redistributing dependency or browser binaries.

Upstream screenshots, WebM examples, fictional evaluation fixtures, and source notices were retained from the exact source commits recorded in `catalog.json`. They were not newly relicensed. Pattern scans and static inspection cannot prove authorship or third-party rights; the owner should confirm ownership of included media and any contributed material before a new public release.

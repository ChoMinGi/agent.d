# Install and use DecisionGuard

DecisionGuard is a skill folder. You need an agent host that supports skills and,
for live Notion work, an authenticated Notion connection. It does not bundle a
server, connector, model API call or workspace data. Python 3.10+ is needed only
for the optional local helpers.

## Codex installer

Ask Codex to install the skill from its repository path:

```text
$skill-installer install https://github.com/ChoMinGi/decisionguard-skill/tree/main/skills/decisionguard
```

To request the v0.6.1 tag rather than the current main branch:

```text
$skill-installer install https://github.com/ChoMinGi/decisionguard-skill/tree/v0.6.1/skills/decisionguard
```

The installer chooses the host's user skill directory. It should inspect an
existing installation before replacing it. You can explicitly invoke the skill
with `$decisionguard`; automatic selection depends on the host and task.

## Manual project installation

Clone the repository:

```sh
git clone https://github.com/ChoMinGi/decisionguard-skill.git
cd decisionguard-skill
```

Copy the whole `skills/decisionguard` folder into the target project's
`.agents/skills/` directory. This example refuses an existing destination; replace
`/path/to/your-project` with the actual project directory:

```sh
skill_target=/path/to/your-project/.agents/skills/decisionguard
if [ -e "$skill_target" ] || [ -L "$skill_target" ]; then
  echo "DecisionGuard already exists here. Inspect it before updating."
else
  mkdir -p /path/to/your-project/.agents/skills
  cp -R skills/decisionguard "$skill_target"
fi
```

Retain `SKILL.md`, `agents/`, `references/` and `scripts/` together. Do not copy
`work/`, workspace exports or reports into the installed skill. Avoid installing
multiple copies with the same name in overlapping discovery locations.

Codex detects skill changes automatically. If the skill is not visible in the
next turn, restart Codex and check its skill settings. See the
[official local skill guide](https://learn.chatgpt.com/docs/build-skills) for current
discovery locations; installations can differ between host versions.

## First use

Start with the [fictional walkthrough](walkthrough.md), which needs no Notion
connection. For a real task, connect Notion through your host and supply an
explicit project location or authorized documents:

```text
Use $decisionguard for this project's feature design. Use only the project
sources I supplied. Recheck any confirmed handoff, apply current decisions,
and keep Notion read-only. Ask only for inputs that affect this design.
```

A source location is needed; no credentials belong in chat. If access is missing,
the skill can work from supplied documents while disclosing that limitation.
It does not automatically retrieve private context from a previous installation.

A request to remember something produces a proposed change and destination.
Confirm the exact change before it is persisted. The next task needs access to
that saved note or ledger and to its current sources. A remembered hypothesis
remains a hypothesis, and an accepted design does not grant release approval.

## Other hosts and updates

Other compatible Agent Skill hosts can load the same folder. Use their documented
skill directory and Notion connection. Cross-host connector compatibility is not
certified by this alpha; no Claude, ChatGPT or other marketplace integration is
bundled here.

To update, inspect and back up any local modifications, then replace only the
installed skill directory with the chosen version. Keep live project memory
outside the installation so an update does not replace it. To uninstall, remove
only that installed copy; project documents and separately stored memory remain.

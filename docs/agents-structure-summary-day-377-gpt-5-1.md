# Day 377 agents.json structure snapshot (GPT-5.1)

This note records a small, read-only structural snapshot of `agents.json` in the
`ai-village-external-agents` repo as of Village Day 377. It does **not** change
any logic, workflows, or external integration behavior.

The companion machine-readable file is:

- `docs/agents-structure-summary-day-377_gpt-5-1.json`

## What this snapshot captures

From the current `agents.json` file:

- **Total agents listed:** 5
- **Affiliations observed:**
  - `#best`: 3 agents
  - `#external`: 1 agent
  - `#guest`: 1 agent
- **Organizations represented:**
  - `AI Village`: 3 agents
  - `Independent (Claudius Maximus)`: 1 agent
  - `Thatfwogguy`: 1 agent
- **Email coverage:**
  - 1 agent with a non-null `email`
  - 4 agents with a missing or null `email`

These values are copied directly from the JSON snapshot so they stay aligned.

## How to use this snapshot

This snapshot is meant as a quick, non-invasive lens on `agents.json`:

- Use the JSON file for programmatic checks on counts by `affiliation`,
  `organization`, and `email` presence without having to re-parse the full
  agents list.
- If `agents.json` evolves in the future (new agents, changed affiliations, or
  more complete emails), you can generate a follow-up snapshot and diff the
  numeric fields in `summary` to see how the external/guest/best mix has
  changed over time.
- Because this file is purely descriptive and lives under `docs/`, it should
  be safe to keep around as historical context without affecting any
  production behavior.

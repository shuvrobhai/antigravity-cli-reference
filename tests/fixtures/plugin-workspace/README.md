# Workspace-Scoped Plugin Agents — Fixture Test (2026-08-11)

Reproducible fixture used to settle the last open plugin-discovery question:
do agents inside **workspace-scoped** plugins (`.agents/plugins/<name>/agents/`)
get discovered and loaded?

## Fixture layout

```
plugin-workspace/
├── .agents/
│   ├── agents/
│   │   └── workspace-control.md      # plain workspace agent (control)
│   └── plugins/
│       └── marker-plugin/
│           ├── plugin.json           # {"name": "marker-plugin"}
│           └── agents/
│               └── marker-agent.md   # workspace-scoped PLUGIN agent
└── README.md
```

Each agent's system prompt demands a distinctive marker reply:

- `marker-agent` → `PLUGIN-MARKER-oklahoma`
- `workspace-control` → `WORKSPACE-MARKER-sierra`

Marker present in the response = that agent's system prompt loaded. Default
agent's generic reply = not loaded.

## Methodology

Run every command from this directory (the fixture workspace is the cwd):

```bash
# 1. Discovery — does agy agents list workspace agents?
agy agents
# Observed: only global + plugin agents (code-reviewer, documentation-writer,
# self-auditor). Neither fixture agent listed. (agy agents has no JSON mode.)

# 2. Loading — headless --agent with the marker prompt
agy -p "Identify yourself exactly." --agent marker-agent --output-format json
agy -p "Identify yourself exactly." --agent workspace-control --output-format json

# 3. Unknown name — silent fallback behavior
agy -p "Identify yourself exactly." --agent definitely-not-an-agent --output-format json
```

## Results (2026-08-11, agy 1.1.11)

| Path | Discovered by `agy agents` | Loaded by headless `-p --agent` | Interactive TUI `/agents` | Verdict |
|---|---|---|---|---|
| Global plugin agent (`self-auditor`) | ✅ listed | ✅ (interactive transcript `a1e51ef2` proves execution) | ✅ | VERIFIED |
| **Workspace plugin agent** (`marker-agent`) | ❌ not listed | ❌ default reply, marker never fired | ✅ listed (user-verified) | **TUI only** |
| Plain workspace agent (`workspace-control`) | ❌ not listed | ❌ default reply, marker never fired | ✅ listed (user-verified) | **TUI only** |
| Unknown name (`definitely-not-an-agent`) | n/a | ✅ "succeeds" with default agent | n/a | SILENT FALLBACK |

## Notes

- `agy agents` is a slow remote fetch (observed ~8 s on a working network; no
  client-side timeout visible — it can appear hung on restricted networks).
- Discovery is **surface-dependent**: the interactive TUI `/agents` selector
  lists workspace-scoped agents (user-verified 2026-08-11), while `agy agents`
  and headless `--agent` ignore them and silently fall back to the default
  agent.
- Results recorded in the research doc (§4.4, §10, §17, §18) and knowledge JSON
  (`extensibility.plugins`, `headless.agent_validation_note`, `hard_gaps`).

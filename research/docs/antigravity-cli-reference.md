# Google Antigravity CLI: Complete Developer Reference and Documentation Gap Analysis

## Version 5.1 — Transcript Audit Edition (2026-08-11)

---

## What This Is

A comprehensive, source-classified reference for every schema, path, configuration key, command, tool, and behavioral specification in Google Antigravity CLI (`agy`), built by systematically auditing 52 sources including the full official documentation at `antigravity.google/docs/*`.

This report answers three questions:

1. **What exists?** — Every configuration key, file path, command, tool argument, and schema in Antigravity CLI.
2. **What do the official docs tell you?** — Everything confirmed at `antigravity.google/docs/*`, with source attribution.
3. **What don't the official docs tell you?** — Behavioral gaps, undocumented contracts, community-sourced findings, and information that requires independent verification.

## Changelog

| Version | Date | Summary |
|---|---|---|
| 1.0 | Initial | Original gap analysis with mixed-sourcing |
| 2.0 | Revision | Tier A/B/C classification applied; sourced vs unsourced separated |
| 3.0 | Major update | All official docs pages incorporated; 50+ sources; schemas expanded |
| 4.0 | Current | Source classification system (`[DOCS]`/`[GOOGLE]`/`[PROTOCOL]`/`[COMMUNITY]`); Sections 16-17 added; 35 commands; 25 behavioral gaps cataloged |
| 5.0 | 2026-08-11 | Live-doc verification run: headless `status` enum + exit codes resolved; `defaultApprovalMode` enum resolved; plugin `agents/` inconsistency confirmed; CLI brain path + transcript schema verified hands-on (new §18.1); Section 10 rebuilt with full flag/stream reference |
| 5.1 | 2026-08-11 | Full-brain transcript audit (`scripts/audit_transcripts.py`, 49,586 lines / 33 sessions): `type` enum expanded to 19 values (9 promoted with citations); `status` enum confirmed as `DONE`/`RUNNING`/`ERROR` (the `ACTIVE` guess superseded); evidence saved under `audits/` |

## How This Report Was Built

1. **Initial audit** — 22 search results retrieved and cross-referenced
2. **Progressive gap identification** — claims classified into Tier A/B/C
3. **Targeted retrieval** — official docs pages retrieved one by one to fill gaps
4. **Source classification** — every claim tagged with `[DOCS]`/`[GOOGLE]`/`[PROTOCOL]`/`[COMMUNITY]`
5. **Behavioral gap cataloging** — every undocumented behavioral question identified
6. **Iterative correction** — claims upgraded, downgraded, or corrected as new sources arrived (5 major revisions)

---

## Table of Contents

1. Executive Summary
2. Methodology and Source Classification
3. Product Ecosystem and Identity
4. Extensibility Architecture
5. Configuration System
6. Permissions Engine
7. Complete CLI Command Reference
8. Built-in Agent Tool API
9. Sandbox
10. Headless Mode
11. Browser Integration
12. Artifacts and Implementation Plans
13. Enterprise Features
14. Workspace Governance Recommendations
15. Complete Path Inventory
16. Information Sourced Outside Official Docs
17. Undocumented Behavioral Contracts
18. Remaining Hard Gaps
    18.1 Transcript Schema (verified hands-on, 2026-08-11)
19. Works Cited

---

## 1. Executive Summary

Google Antigravity CLI (`agy`) is a lightweight, terminal-first interface for directing autonomous coding agents, executing shell commands, and managing background subagents entirely from the keyboard. It is the terminal component of the broader Google Antigravity ecosystem, which also includes Antigravity 2.0 (standalone desktop application), Antigravity IDE, and the Antigravity SDK.

The platform's extensibility architecture is built on open, portable standards: Markdown files with YAML frontmatter for Skills, Agents, Rules, and Workflows; the Model Context Protocol (MCP) for tool integrations; and JSON configuration files for hooks and settings. This design ensures customizations are portable across Claude Code, Cursor, Codex CLI, and any other tool adopting the same standards.

This report documents every confirmed configuration key, path, schema, command, and behavioral specification available from official documentation (`antigravity.google/docs/*`), while clearly identifying information sourced from other channels and cataloging behavioral questions the official docs leave unanswered.

---

## 2. Methodology and Source Classification

### Confidence Tiers

Every claim is classified:

| Tier | Label | Definition |
|---|---|---|
| **A** | **Confirmed by Sources** | Directly stated in a retrieved source. Safe to rely on for production decisions. |
| **B** | **Reasonable Inference** | Logically extrapolated from confirmed information. Validate before production reliance. |
| **C** | **Requires Independent Verification** | Not found in any retrieved source. Must be tested against a live installation. |

### Source Classification

Every claim is tagged with its source origin:

| Tag | Scope | Authority |
|---|---|---|
| `[DOCS]` | `antigravity.google/docs/*` | Official product documentation. Primary authority. |
| `[GOOGLE]` | Other Google-owned sources (Codelabs at `codelabs.developers.google.com`, Gemini CLI docs at `google.github.io/gemini-cli`, Google AI for Developers at `ai.google.dev`, Google Cloud at `cloud.google.com`) | High reliability. May lag behind main docs or reflect legacy behavior. |
| `[PROTOCOL]` | `modelcontextprotocol.io` | Official MCP specification. Authoritative for MCP protocol details. |
| `[COMMUNITY]` | Third-party sources (blogs, tutorials, security research, Reddit, GitHub, partner docs) | Variable reliability. Included only when official docs are silent. Explicitly called out. |

### How to Read This Report

- Claims tagged `[DOCS]` can be treated as authoritative product documentation.
- Claims tagged `[GOOGLE]` are reliable but may reflect legacy (Gemini CLI) behavior that has changed in Antigravity CLI. Verify when possible.
- Claims tagged `[COMMUNITY]` represent third-party observations or recommendations. Treat as supplementary intelligence, not product specification.
- **Section 16** consolidates all information sourced outside official docs in one reference table.
- **Section 17** catalogs every behavioral question the official docs leave unanswered.

---

## 3. Product Ecosystem and Identity

### 3.1 Product Family

Google Antigravity comprises four products `[DOCS]`:

| Product | Description | Interface |
|---|---|---|
| **Antigravity 2.0** | Standalone desktop application. Command center for managing multiple local agents, grouped projects, workspaces, and scheduled tasks. | GUI application |
| **Antigravity IDE** | Fully-featured agentic IDE with agent manager, artifacts, and deep codebase understanding. VS Code fork. | IDE |
| **Antigravity CLI** | Lightweight, fast, terminal-first surface for autonomous coding agents, shell execution, and background subagent management. | Terminal (`agy`) |
| **Antigrativity SDK** | Python SDK for programmatic integration, custom agent prototyping, and automated evaluations. | Python API |

### 3.2 CLI Technical Characteristics

- **Language:** Written in Go `[GOOGLE]`
- **Optimized model:** Gemini 3.5 Flash, optimized for the Antigravity harness `[GOOGLE]`
- **Architecture:** Asynchronous-first — subagents run in the background, commands execute asynchronously, terminal remains ready at all times `[GOOGLE]`
- **Binary:** `agy` for CLI; `antigravity` for desktop IDE `[GOOGLE]`
- **Config tree:** Reuses `~/.gemini/` directory for backward compatibility `[GOOGLE]`

### 3.3 System Requirements

| Platform | Requirement |
|---|---|
| **macOS** | macOS 12 (Monterey) minimum. Apple Silicon only (x86 NOT supported). Current + two previous versions with Apple security update support. |
| **Windows** | Windows 10 (64-bit) |
| **Linux** | glibc >= 2.28, glibcxx >= 3.4.25 (Ubuntu 20, Debian 10, Fedora 36, RHEL 8) |

**Source:** `[DOCS]`

### 3.4 Migration from Gemini CLI

Starting June 18, 2026, Gemini Code Assist IDE extensions and Gemini CLI stopped serving requests for consumer tiers `[GOOGLE]`. Enterprise subscriptions remain unaffected.

**Configuration migration mapping:** `[GOOGLE]`

| Configuration | Gemini CLI (Legacy) | Antigravity CLI (Current) |
|---|---|---|
| User settings | `~/.gemini/settings.json` | `~/.gemini/antigravity-cli/settings.json` |
| Global shared skills | `~/.gemini/skills/` | `~/.gemini/config/skills/` |
| Workspace project skills | `.gemini/skills/` | `.agents/skills/` |

### 3.5 Model Ecosystem

`[DOCS]`

| Model | Free & AI Plus | AI Pro | AI Ultra | Enterprise |
|---|---|---|---|---|
| Gemini 3.6 Flash | Yes | Yes | Yes | Yes |
| Gemini 3.5 Flash | Yes | Yes | Yes | Yes |
| Gemini 3.1 Pro | Yes | Yes | Yes | Yes |
| Claude Sonnet 4.6 (thinking) | Yes | Yes | Yes | **No** |
| Claude Opus 4.6 (thinking) | Yes | Yes | Yes | **No** |
| GPT-OSS-120b | Yes | Yes | Yes | **No** |

**Nano Banana 2** is used internally for generative image tasks `[GOOGLE]`.

Model selection is "sticky" within a conversation `[DOCS]`.

### 3.6 Open Standards Foundation

The entire extensibility architecture is built on portable, open standards:

| Component | Format | Cross-Tool Portability | Source |
|---|---|---|---|
| **MCP** | Open protocol | Claude, ChatGPT, VS Code, Cursor, MCPJam | `[DOCS]` + `[PROTOCOL]` |
| **Skills** | `SKILL.md` with YAML frontmatter | Claude Code, Cursor, Codex CLI | `[DOCS]` confirms format; `[COMMUNITY]` confirms cross-tool portability |
| **Agents** | `.md` with YAML frontmatter | Same format pattern | `[DOCS]` |
| **Rules** | `.md` constraint files | Markdown — inherently portable | `[DOCS]` |
| **Workflows** | `.md` step sequences | Markdown — inherently portable | `[DOCS]` |

MCP is described as "an open-source standard" using a USB-C analogy for AI apps `[DOCS]`.

---

## 4. Extensibility Architecture

Antigravity CLI supports seven extensibility mechanisms.

### 4.1 Progressive Disclosure Engine

This is an officially documented three-phase design pattern `[DOCS]`:

| Phase | What Loads | When | Token Cost |
|---|---|---|---|
| **Phase 1 — Metadata** | `name` and `description` from YAML frontmatter | Session start | ~100 tokens per skill `[GOOGLE]` |
| **Phase 2 — Instructions** | Full `SKILL.md` body | Agent determines relevance | <5,000 tokens recommended `[GOOGLE]` |
| **Phase 3 — Resources** | `scripts/`, `examples/`, `resources/` subdirectories | On demand | Variable |

**Phase 1 token costs and Phase 2 size recommendations** come from the Agent Skills 101 Codelab `[GOOGLE]`, not from the official docs pages.

### 4.2 Skills System

**Definition:** Skills are an open standard for extending agent capabilities. A skill is a folder containing a `SKILL.md` file with instructions that the agent can follow `[DOCS]`.

Skills are agent-triggered — the model detects intent and dynamically loads relevant skills. Unlike System Prompts (always loaded), Skills load on demand `[DOCS]`.

**Paths:** `[DOCS]`

| Scope | Path |
|---|---|
| **Global** | `~/.gemini/config/skills/<skill-folder>/` |
| **Workspace** | `<workspace-root>/.agents/skills/<skill-folder>/` |

Note: `.agent/skills` (singular) supported for backward compatibility `[DOCS]`.

**SKILL.md Format:** `[DOCS]`

```
---
name: my-skill
description: Helps with a specific task. Use when you need to do X or Y.
---

# My Skill

Detailed instructions for the agent go here.

## When to use this skill
- Use this when...

## How to use it
Step-by-step guidance...
```

**Frontmatter Specification:** `[DOCS]`

| Field | Required | Default | Description |
|---|---|---|---|
| `name` | **No** | Folder name | Unique identifier (lowercase, hyphens) |
| `description` | **Yes** | — | What the skill does and when to use it |

**These are the only two frontmatter fields for Skills.** Attributes such as `disable-model-invocation`, `argument-hint`, and `user-invocable` are not documented in official sources. For granular execution control, use Custom Agents (Section 4.3).

**Tip:** Write descriptions in third person with keywords for recognition. Example: "Generates unit tests for Python code using pytest conventions." `[DOCS]`

**Folder Structure:** `[DOCS]`

```
.agents/skills/my-skill/
├── SKILL.md       # Main instructions (required)
├── scripts/       # Helper scripts (optional)
├── examples/      # Reference implementations (optional)
└── resources/     # Templates and other assets (optional)
```

**Progressive Disclosure Behavior:** `[DOCS]`

1. **Discovery:** Agent sees skill names and descriptions at session start
2. **Activation:** If relevant, agent reads full `SKILL.md` content
3. **Execution:** Agent follows instructions while working

Explicit mention of a skill by name ensures use, but is not required `[DOCS]`.

**Best Practices:** `[DOCS]`

- Keep skills focused — one skill per distinct task
- Write clear, specific descriptions
- Use scripts as black boxes — encourage `--help` first
- Include decision trees for complex skills

### 4.3 Custom Agents

**Definition:** Reusable persona definitions in Markdown format with YAML frontmatter. Define *who* the agent is (capabilities, tools, execution policy, model) rather than *what* to do `[DOCS]`.

Two creation paths:

1. **File-based:** `.agents/agents/<name>.md` — persistent, discoverable
2. **Tool-based:** `define_subagent` tool — ephemeral, session-scoped

**Discovery Locations:** `[DOCS]`

| Location | Path | Scope |
|---|---|---|
| Workspace | `.agents/agents/<name>.md` or `.agents/agents/<name>/agent.md` | Repository |
| Global | `~/.gemini/config/agents/<name>.md` or `.../agents/<name>/agent.md` | Machine-wide |
| Plugins | `plugins/<plugin_name>/agents/` | Bundled package |

**Frontmatter Specification:** `[DOCS]`

| Property | Type | Default | Description |
|---|---|---|---|
| `name` | string | **Required** | Unique identifier |
| `description` | string | **Required** | Used by planner to determine delegation |
| `tools` | string[] | `[]` | Permitted tools (e.g., `view_file`, `run_command`) |
| `mainAgent` | boolean | `true` | Allow selection as primary agent in chat |
| `subagent` | boolean | `true` | Allow invocation via `invoke_subagent` |
| `model` | string | `inherit` | Model tier (`inherit`, `flash`, `pro`) |
| `commandExecutionPolicy` | string | `sandbox` | Shell command policy (`off`, `auto`, `eager`, `sandbox`) |
| `mcpServers` | object[] | `[]` | Custom MCP servers for this subagent |
| `skills` / `plugins` | string[] | `[]` | Skill paths or plugin dependencies |

**Known Issue (documented):** Misspelled tool names in the `tools` list may cause the subagent to hang. Fix planned `[DOCS]`.

**Example (`code-auditor.md`):** `[DOCS]`

```yaml
---
name: code-auditor
description: Specialized subagent for security audits, static analysis, and code quality reviews.
tools:
  - view_file
  - grep_search
  - run_command
subagent: true
mainAgent: false
model: pro
commandExecutionPolicy: sandbox
skills:
  - skills/security-checklist
---

# System Prompt
You are an expert security auditor and code reviewer.

# Review Guidelines
1. Perform thorough static analysis without altering files unless explicitly asked.
2. Flag potential injection flaws, unvalidated inputs, or hardcoded secrets.
3. Provide concise, actionable remediation steps.
```

**Built-in Subagents:** `[DOCS]`

| Name | Purpose | Invocation |
|---|---|---|
| `research` | Codebase research, file navigation, structural exploration | Via `invoke_subagent` |
| `browser` | Sandboxed web browser testing | Exclusively via `/browser` |
| `self` | Clone of calling agent with identical system instructions and toolsets | Via `invoke_subagent` |

**Subagent Lifecycle States:** `[DOCS]`

| State | Behavior |
|---|---|
| **Running** | Actively executing. Can be cancelled (`k` in CLI) or interrupted by parent. |
| **Idle** | Task completed, result sent to parent, paused. Auto-re-awakens on incoming message. Retains all context from prior turns. |
| **Killed** | Permanently terminated. Worktrees cleaned up. Historical transcripts remain in JSONL logs. |

**Inter-Agent Communication:** `[DOCS]`

| Aspect | Detail |
|---|---|
| Routing | Via unique agent conversation IDs |
| Topology | Parent ↔ subagent, peer ↔ peer (if ID known) |
| Auto-Wake | Messages to idle subagents trigger re-awakening |
| Shared Transcripts | Agents can read each other's conversation transcripts |
| Nesting Limit | **Maximum 10 levels** (strictly enforced) |

**Permissions Inheritance:** `[DOCS]`

Subagents inherit terminal command prefixes, file read/write scopes, and sandbox settings from parent. Parent retains full access to subagent workspaces. Tool authorization requests bubble up to the main UI.

**Multi-Agent Teamwork:** `[DOCS]`

| Aspect | Detail |
|---|---|
| Command | `/teamwork-preview` |
| Availability | Ultra Plan ($200/mo) only |
| Status | Preview |
| Features | Error recovery, automatic retries, task coordination |

**Workspace Options:** `[DOCS]`

| Mode | Behavior |
|---|---|
| `inherit` | Read-only copy of parent workspace |
| `branch` | Isolated Git worktree (read-write, merge-back) |
| `share` | Direct access to parent workspace |

### 4.4 Plugins

**Definition:** Namespaced bundles that group skills, rules, MCP servers, and hooks into a single package `[DOCS]`.

**Directory Structure:** `[DOCS]`

```
plugins/<plugin-name>/
├── plugin.json       # Required marker file
├── mcp_config.json   # Optional MCP server definitions
├── hooks.json        # Optional hooks definition
├── skills/           # Optional skills
│   └── <skill-name>/
│       └── SKILL.md
└── rules/            # Optional rules
    └── <rule-name>.md
```

**Manifest (`plugin.json`):** `[DOCS]`

```json
{
  "name": "my-custom-plugin"
}
```

The `name` field is **optional** — defaults to directory name.

**Supported Components:** `[DOCS]` — Skills, Rules, MCP Servers, Hooks (4 components). **Verified hands-on 2026-08-11:** plugins also support `agents/` and `commands` components — the plugins page directory structure is **incomplete**.

**Agents component (verified hands-on):** The subagents page references `plugins/<plugin_name>/agents/` as a discovery location and the plugins page omits it — the **subagents page is correct**. Evidence chain: (1) `agy plugin list` reports `agents` as a component of installed plugins, e.g. `self-customizer` (source: `antigravity`), which ships `~/.gemini/config/plugins/self-customizer/agents/self-auditor.md`; (2) `agy agents` lists `self-auditor` alongside global agents — it is discoverable as a loadable agent. (Workspace-scoped `.agents/plugins/` agent discovery was **MEASURED 2026-08-11 — NOT surfaced on the CLI/headless surfaces**: a fixture workspace containing `.agents/plugins/marker-plugin/agents/marker-agent.md` and a plain `.agents/agents/workspace-control.md` was probed; `agy agents` run from inside that workspace listed only the three global/plugin agents, and headless `-p --agent <name>` for both fixture agents produced the default agent's generic reply — the marker system prompts never fired. `agy agents` also has no `--output-format json` mode. **Interactive TUI `/agents` DOES list workspace-scoped agents** (user-verified 2026-08-11) — discovery is surface-dependent: TUI = global + plugin + workspace; headless/CLI = global + plugin only, with silent fallback for anything else. Fixture preserved in the repo at `tests/fixtures/plugin-workspace/`.)

**Commands component (observed):** Plugins imported from gemini-cli / claude-code carry a `commands` component (e.g. `ponytail`, `product-management`) — also absent from the plugins page.

**plugin.json `$schema`:** Installed antigravity plugins reference `https://antigravity.google/schemas/v1/plugin.json` — an official JSON Schema exists for plugin manifests `[B]`.

**Management surface (verified hands-on):** `agy plugin <command>` — `list` (JSON: `imports[]` with `name`, `source` (`antigravity`/`gemini-cli`/`claude-code`), `importedAt`, `components[]`), `import [source]`, `install <target>` (supports `plugin@marketplace`), `uninstall`, `enable`, `disable`, `validate [path]`, `link`.

**Discovery Paths:** `[DOCS]`

| Scope | Path |
|---|---|
| Workspace | `.agents/plugins/` or `_agents/plugins/` |
| Global | `~/.gemini/config/plugins/` |

**Adding Plugins:** `[DOCS]`

| Method | Description |
|---|---|
| Bundled (Build with Google) | Browse from Customizations page |
| Manual | Place in workspace or global plugin directories |

### 4.5 Model Context Protocol (MCP)

**Definition:** Open standard connecting AI agents to local developer tools, databases, file parsers, and remote APIs `[DOCS]` + `[PROTOCOL]`.

**Configuration Paths:** `[DOCS]`

| Scope | Path |
|---|---|
| Global | `~/.gemini/config/mcp_config.json` |
| Workspace | `.agents/mcp_config.json` |

**Configuration Structure:** `[DOCS]`

```json
{
  "mcpServers": {
    "sqlite-explorer": {
      "command": "node",
      "args": ["/usr/local/bin/sqlite-mcp-server.js"],
      "env": { "SQLITE_DB_PATH": "/var/data/app.db" }
    },
    "my-remote-server": {
      "serverUrl": "https://api.example.com/mcp/",
      "headers": { "Authorization": "Bearer YOUR_API_TOKEN" }
    }
  }
}
```

**Configuration Properties:** `[DOCS]`

*Transport (one required):*

| Property | Type | Transport | Description |
|---|---|---|---|
| `command` | string | Stdio | Path to executable |
| `serverUrl` | string | Remote | **Required** for SSE, Streamable HTTP, or websocket connections |

**Warning:** Legacy fields `url` and `httpUrl` are **not supported** in Antigravity CLI. You must use `serverUrl` `[DOCS]`.

*Optional:*

| Property | Type | Description |
|---|---|---|
| `args` | string[] | CLI arguments for Stdio |
| `env` | object | Environment variables. Supports `$VAR`, `${VAR}`, `${VAR:-default}`, `%VAR%` (Windows) |
| `cwd` | string | Working directory for Stdio |
| `headers` | object | Custom HTTP headers for remote servers |
| `authProviderType` | string | `"google_credentials"` for Google ADC |
| `oauth` | object | `{clientId, clientSecret}` for manual OAuth |
| `disabled` | boolean | Temporarily disable without removing |
| `disabledTools` | string[] | Withhold specific tools from model |
| `timeout` | number | Request timeout |

**Authentication:** `[DOCS]`

| Method | Configuration | Details |
|---|---|---|
| Google Credentials | `"authProviderType": "google_credentials"` | Requires `gcloud auth application-default login` |
| OAuth (DCR) | No additional config | Automatic for servers supporting Dynamic Client Registration |
| OAuth (Manual) | `"oauth": {"clientId": "...", "clientSecret": "..."}` | Redirect URI: `https://antigravity.google/oauth-callback` |
| Custom Headers | `"headers": {"Authorization": "Bearer ..."}` | For API keys or bearer tokens |

**OAuth Token Storage:** `~/.gemini/antigravity/mcp_oauth_tokens.json` `[DOCS]`. Auto-refresh on expiry; auto-remove on invalidation.

**MCP Permissions:** `[DOCS]`

| Target Pattern | Scope |
|---|---|
| `mcp(server/tool)` | Specific tool on specific server |
| `mcp(server/*)` | All tools on specified server |
| `mcp(*)` | Any MCP tool across all servers |

Unconfigured MCP tools default to Ask mode.

**Interactive MCP Manager:** `/mcp` command. View status rings, reload configs, inspect logs `[DOCS]`.

**MCP Store:** 50+ direct integrations including AlloyDB, BigQuery, Bigtable, Chrome DevTools, ClickHouse, Cloud SQL (MySQL/PostgreSQL/SQL Server), Dataplex, Figma, Firebase, GitHub, GitLab, GKE, Heroku, Linear, MongoDB, Neon, Netlify, Notion, PayPal, Perplexity, Pinecone, PostHog, Postman, Prisma, Redis, Stripe, Supabase, and more `[DOCS]`.

**SDK Integration:** Antigravity SDK auto-discovers servers from `.agents/mcp_config.json` `[DOCS]`.

### 4.6 Rules

**Definition:** Markdown files defining constraints or guidelines for agent behavior `[DOCS]`.

| Scope | Path |
|---|---|
| Global | `~/.gemini/GEMINI.md` |
| Workspace | `.agents/rules/` |

Backward compat: `.agent/rules` (singular) `[DOCS]`.

**Size Limit:** 12,000 characters per rule file `[DOCS]`.

**Activation Modes:** `[DOCS]`

| Mode | Behavior |
|---|---|
| `Manual` | Activated via @ mention |
| `Always On` | Always applied |
| `Model Decision` | Agent decides based on rule description |
| `Glob` | Applied to files matching a pattern |

**@ File References:** Relative paths resolve from rules file location; absolute paths resolve directly; otherwise relative to repository `[DOCS]`.

### 4.7 Workflows

**Definition:** Markdown files with title, description, and step sequences `[DOCS]`.

| Aspect | Detail |
|---|---|
| Invocation | `/workflow-name` |
| Scope | Global or Workspace |
| Composition | Workflows can call other workflows |
| Execution | Sequential |
| Management | Customizations panel |

**Distinction from Rules:** Rules = persistent context at prompt level. Workflows = structured sequences at trajectory level `[DOCS]`.

### 4.8 Lifecycle Hooks

**Definition:** Run custom scripts at specific points during the execution loop `[DOCS]`.

**Configuration Paths:** `[DOCS]`

| Scope | Path |
|---|---|
| Workspace | `.agents/hooks.json` |
| Global | `~/.gemini/config/hooks.json` |

**Hook Schema:** `[DOCS]`

```json
{
  "my-linter-hook": {
    "PostToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/lint.sh",
            "timeout": 10
          }
        ]
      }
    ]
  },
  "safety-gate": {
    "enabled": false,
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [{ "command": "./scripts/safety-check.sh" }]
      }
    ]
  }
}
```

**Hook Definition Fields:** `[DOCS]`

| Field | Type | Description |
|---|---|---|
| `enabled` | Boolean | Optional. `false` to disable without removing. Default `true`. |
| `PreToolUse` | Array | Before tool execution |
| `PostToolUse` | Array | After tool completion |
| `PreInvocation` | Array | Before model call |
| `PostInvocation` | Array | After model invocation |
| `Stop` | Array | When execution terminates |

**Confirmed Lifecycle Events:** `[DOCS]`

| Event | Description | Matcher Target |
|---|---|---|
| `PreToolUse` | Before tool execution | Tool name |
| `PostToolUse` | After tool completion | Tool name |
| `PreInvocation` | Before model call | N/A |
| `PostInvocation` | After model invocation | N/A |
| `Stop` | Execution terminates | N/A |

**Note:** Community sources reference `AfterAgent` and `AfterTool` event names `[COMMUNITY]`. These may be aliases for `PostInvocation` and `PostToolUse`. Discrepancy unresolved.

**Matcher Patterns:** `[DOCS]`

| Pattern | Behavior |
|---|---|
| `""` or `"*"` | Match all tools |
| `"run_command"` | Match exactly |
| `"run_command\|view_file"` | Match either |
| `"browser_.*"` | Regex prefix match |

**IPC:** JSON stdin/stdout. Non-zero exit from `PreToolUse` cancels execution `[DOCS]`.

### 4.9 Component Relationships

`[DOCS]`

| Component | Analogy | Nature | Loading |
|---|---|---|---|
| MCP Servers | "Hands" | Persistent external connections | Always connected |
| Skills | "Brains" | Ephemeral task definitions | On-demand |
| Rules | "Laws" | Global constraints | Always loaded |
| Workflows | "Playbooks" | Multi-step orchestrations | On-demand |
| Agents | "Personas" | Capability profiles | On invocation |
| Plugins | "Packages" | Bundled combinations | On installation |
| Hooks | "Guards" | Lifecycle interceptors | Event-triggered |

---

## 5. Configuration System

### 5.1 Settings File

`~/.gemini/antigravity-cli/settings.json` `[DOCS]`

### 5.2 Sparse Persistence

The CLI writes only values that differ from system defaults. This keeps config files clean and forward-compatible. Updated defaults from Google are automatically inherited `[DOCS]`.

### 5.3 Configuration Precedence

Seven-level hierarchy confirmed for Gemini CLI `[GOOGLE]`. Antigravity CLI likely inherits:

| Level | Source | Scope |
|---|---|---|
| 1 | Default values | Hardcoded |
| 2 | System defaults file | `/etc/gemini-cli/system-defaults.json` (Linux), `C:\ProgramData\gemini-cli\system-defaults.json` (Windows), `/Library/Application Support/GeminiCli/system-defaults.json` (macOS). Overridable via `GEMINI_CLI_SYSTEM_DEFAULTS_PATH` |
| 3 | User settings | `~/.gemini/settings.json` |
| 4 | Project settings | `.gemini/settings.json` |
| 5 | System settings | `/etc/gemini-cli/settings.json` (Linux), `C:\ProgramData\gemini-cli\settings.json` (Windows), `/Library/Application Support/GeminiCli/settings.json` (macOS). Overridable via `GEMINI_CLI_SYSTEM_SETTINGS_PATH` |
| 6 | Environment variables | Shell variables, `.env` files |
| 7 | Command-line arguments | `agy --sandbox --model="Gemini 3.5 Flash"` |

### 5.4 Environment Variable Interpolation

String values support `$VAR_NAME`, `${VAR_NAME}`, `${VAR_NAME:-DEFAULT_VALUE}` `[GOOGLE]`. Each plugin can have its own `.env` file.

### 5.5 Complete settings.json Schema

#### Safety and Permissions `[DOCS]`

| Key | Type | Default | Options |
|---|---|---|---|
| `toolPermission` | string | `"request-review"` | `request-review`, `proceed-in-sandbox`, `always-proceed`, `strict` |
| `artifactReviewPolicy` | string | `"asks-for-review"` | `asks-for-review`, `agent-decides`, `always-proceed` |
| `enableTerminalSandbox` | boolean | `false` | `true`, `false` |
| `allowNonWorkspaceAccess` | boolean | `false` | `true`, `false` |
| `trustedWorkspaces` | string[] | `[]` | Whitelist of authorized repository paths |

#### Display and Rendering `[DOCS]`

| Key | Type | Default | Options |
|---|---|---|---|
| `colorScheme` | string | `"terminal"` | `light`, `solarized light`, `colorblind-friendly light`, `dark`, `solarized dark`, `colorblind-friendly dark`, `tokyo night`, `terminal` |
| `altScreenMode` | string | `"default"` | `default`, `always`, `never` |
| `notifications` | boolean | `false` | `true`, `false` |
| `showTips` | boolean | `true` | `true`, `false` |
| `showFeedbackSurvey` | boolean | `true` | `true`, `false` |
| `ui.language` | string | `"us"` | Interface language |
| `ui.footer.items` | string[] | standard items | Footer display widgets (`model-name`, `agent-profile`, `agent-state`, `context-used`, `token-count`, `artifacts`, `quota`, `quota-weekly`, `project-path`) |

#### Editor `[DOCS]`

| Key | Type | Default | Options |
|---|---|---|---|
| `editor` | string | `"auto"` | `auto`, `vim`, `emacs`, `nano`, or any binary |
| `editorMode` | string | `"default"` | `default`, `vim` |
| `vimInsertFirst` | boolean | `false` | `true`, `false` (requires `editorMode: "vim"`) |

#### Behavior `[DOCS]`

| Key | Type | Default | Options |
|---|---|---|---|
| `verbosity` | string | `"high"` | `high`, `low` |
| `runningLightSpeed` | string | `"medium"` | `fast`, `medium`, `slow`, `off` |
| `useG1Credits` | boolean | `false` | `true`, `false` (external builds only) |
| `enableTelemetry` | boolean | `true` | `true`, `false` |
| `model` | string | (unset) | Model display name + effort tier, e.g. `"Gemini 3.5 Flash (Low)"` |

> **`model` (verified 2026-08-11 via config diff + live probe `[GOOGLE]`/A):** Not listed on the antigravity.google settings page — discovered by diffing the live config (`scripts/diff_settings.py`). Confirmed hands-on: a headless `agy -p` run with **no** `--model` flag resolved the session's `Model Selection` to the configured value (`Gemini 3.5 Flash (Low)`), proving the key is the persisted default-model setting. Value format matches the documented `--model="Gemini 3.5 Flash"` flag format; effort tier (`Low`/`High`) is part of the value.

#### Custom Scripts `[DOCS]`

| Key | Type | Description |
|---|---|---|
| `title` | object | `{"type": "command", "command": "<path>"}` |
| `statusLine` | object | `{"type": "command", "command": "<path>", "padding": 0, "enabled": true, "stack_with_default": false}` |

#### Permissions `[DOCS]`

| Key | Type | Description |
|---|---|---|
| `permissions.allow` | string[] | Allowlist rules |
| `permissions.deny` | string[] | Denylist rules |
| `permissions.ask` | string[] | Asklist rules |

#### General (Gemini CLI confirmed) `[GOOGLE]`

| Key | Type | Default | Description |
|---|---|---|---|
| `general.preferredEditor` | enum | `undefined` | `vscode`, `vscodium`, `windsurf`, `cursor`, `zed`, `antigravity`, `sublimetext`, `lapce`, `nova`, `bbedit`, `vim`, `neovim`, `emacs`, `hx`, `emacsclient`, `micro` |
| `general.openEditorInNewWindow` | boolean | `false` | New window for VS Code-family |
| `general.vimMode` | boolean | `false` | Vim keybindings |
| `policyPaths` | array | `[]` | Additional policy files (requires restart) |
| `adminPolicyPaths` | array | `[]` | Additional admin policy files (requires restart) |

### 5.6 Status Line JSON Payload

Custom scripts receive this JSON via stdin `[DOCS]`:

| Field | Type | Description |
|---|---|---|
| `cwd` | string | Current working directory |
| `session_id` / `conversation_id` | string | Session identifier |
| `transcript_path` | string | Path to transcript log |
| `model` | object | `{id, display_name}` |
| `workspace` | object | `{current_dir, project_dir}` |
| `version` | string | CLI version |
| `context_window` | object | Token usage: `total_input_tokens`, `total_output_tokens`, `context_window_size`, `used_percentage`, `remaining_percentage`, plus `current_usage` sub-object (`input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`) |
| `exceeds_200k_tokens` | bool/null | Context > 200k flag |
| `product` | string | Application name |
| `quota` | object | Maps model/bucket IDs (e.g. `gemini-weekly`) to `{remaining_fraction, reset_time, reset_in_seconds}` |
| `agent_state` | string | `idle`, `thinking`, `working`, `tool_use`, `initializing` |
| `vcs` | object | `{type, branch, client, dirty}` — type: `git`, `jj`, or `hg` |
| `sandbox` | object | `{enabled, allow_network}` |
| `artifact_count` | int | Artifacts produced |
| `plan_tier` | string | Subscription tier |
| `email` | string | Authenticated user |
| `pending_input_count` | int | Queued messages |
| `tool_confirmation_pending` | bool | Confirmation dialog showing |
| `task_count` | int | Background tasks |
| `terminal_width` | int | Terminal width |
| `execution_mode` | string | `planning`, `fast` |
| `vim` | object | `{mode}` — `NORMAL`, `INSERT`, `VISUAL`, `VISUAL LINE` |

Title scripts receive the same payload `[DOCS]`.

### 5.7 Keybindings

**File:** `~/.gemini/antigravity-cli/keybindings.json` `[DOCS]`

**Format:** JSON mapping action strings to hotkey arrays. Empty array `[]` disables. Malformed entries fall back to defaults. Delete file to restore all defaults `[DOCS]`.

**Complete TUI Command Inventory:** `[DOCS]`

| Category | TUI Command | Default Hotkey(s) |
|---|---|---|
| Global | `cli.escape` | `Escape` |
| Global | `cli.exit` | `Ctrl+C` (empty prompt) |
| Global | `cli.clear_screen` | `Ctrl+L` |
| Prompt | `prompt.submit` | `Enter` |
| Prompt | `prompt.newline` | `Shift+Enter`, `Ctrl+J` |
| Prompt | `edit.open_editor` | `Ctrl+G` |
| Prompt | `clipboard.paste_image` | `Ctrl+V` |
| Prompt | `prompt.insert_file` | `@` |
| Navigation | `nav.scroll_line` | `↑`, `↓` |
| Navigation | `nav.scroll_half_page` | `Shift+Page Up/Down`, `Ctrl+U/D` |
| Navigation | `nav.scroll_top` | `Home` |
| Navigation | `nav.scroll_bottom` | `End` |
| Navigation | `nav.focus_top` | `>` |
| Navigation | `nav.focus_bottom` | `<` |
| Navigation | `nav.tab_forward` | `Tab` |
| Navigation | `nav.tab_backward` | `Shift+Tab` |
| Confirmations | `confirm.approve` | `y` |
| Confirmations | `confirm.reject` | `n` |
| Confirmations | `confirm.approve_all` | `Shift+A` |
| Confirmations | `confirm.reject_all` | `Shift+R` |
| Confirmations | `confirm.preview` | `p` |
| Confirmations | `nav.confirm` | `Enter` |
| Confirmations | `nav.escape` | `Escape` |
| Confirmations | `nav.switch_button` | `Tab` |

### 5.8 Context Rule Files `[DOCS]`

| File | Scope |
|---|---|
| `GEMINI.md` (project root) | Workspace context rules |
| `AGENTS.md` (project root) | Agent-specific rules |
| `~/.gemini/GEMINI.md` | Global context rules |

### 5.9 Interactive Settings `[DOCS]`

Type `/config` or `/settings`. Navigate with arrows. Enter to toggle. Escape to save. CLI flags override for session duration with warning indicator.

---

## 6. Permissions Engine

### 6.1 Macro Level

`toolPermission` setting controls broad authorization flow `[DOCS]`:

| Mode | Behavior |
|---|---|
| `request-review` | Prompts for write/bash/web tools (default) |
| `proceed-in-sandbox` | Auto-runs if sandboxed; otherwise prompts |
| `strict` | Prompts for all non-read tools |
| `always-proceed` | No prompts |

### 6.2 Fine-Grained Level

```json
{
  "permissions": {
    "allow": ["command(git)", "read_file(/var/log/app)"],
    "deny": ["command(rm -rf)", "command(sudo)"],
    "ask": ["command(*)", "execute_url(aws.amazon.com)"]
  }
}
```

**Precedence:** Deny > Ask > Allow `[DOCS]`.

### 6.3 Action Types `[DOCS]`

| Action | Target | Default |
|---|---|---|
| `read_file` | path or `*` | Ask (workspace auto-allowed) |
| `write_file` | path or `*` | Ask (workspace auto-allowed) |
| `read_url` | domain or `*` | Ask |
| `execute_url` | domain or `*` | Ask |
| `command` | prefix/regex or `*` | Ask |
| `unsandboxed` | prefix or `*` | Ask |
| `mcp` | server/tool or `*` | Ask |

### 6.4 Implicit Rules `[DOCS]`

- Write implies Read (allowing `write_file` auto-grants `read_file`)
- Deny Read implies Deny Write
- Cross-platform path normalization applied

### 6.5 Default Behaviors `[DOCS]`

1. Workspace read/write = auto-allowed
2. Web browsing = Ask
3. Everything else = Ask

### 6.6 Browser Security `[DOCS]`

| Layer | Mechanism | Behavior |
|---|---|---|
| Denylist | Server-side (Google BadUrlsChecker) | Checked via RPC. Server unavailable = deny. Cannot be overridden. |
| Allowlist | Local text file | Initialized with `localhost`. Denylist takes precedence. |

### 6.7 Agent Settings (Desktop) `[DOCS]`

- **Terminal Command Auto Execution:** `Request Review` (default) or `Always Proceed`
- **Non-Workspace File Access:** Disabled by default. Agent limited to project folders + `~/.gemini/antigravity/`

### 6.8 Permission Inheritance `[DOCS]`

Subagents inherit terminal command prefixes, file scopes, and sandbox settings. Authorization requests bubble up to main UI.

---

## 7. Complete CLI Command Reference

35 confirmed slash commands:

### Core `[DOCS]`

| Command | Alias | Description |
|---|---|---|
| `/exit` | `/quit` | Close TUI |

### Conversations `[DOCS]`

| Command | Alias | Description |
|---|---|---|
| `/resume` | `/switch`, `/conversation` | Browse, search, resume past conversations |
| `/fork` | `/branch` | Clone conversation or fork to different project |
| `/rename <name>` | — | Rename session |
| `/rewind` | `/undo` | Roll back to previous message |

### Configurations `[DOCS]`

| Command | Alias | Description |
|---|---|---|
| `/config` | `/settings` | Interactive settings editor |
| `/model` | — | Choose reasoning model |
| `/fast` | — | Enable fast mode |
| `/planning` | — | Enable planning mode |
| `/keybindings` | — | Keyboard shortcut editor |

### Agent Control `[DOCS]`

| Command | Alias | Description |
|---|---|---|
| `/agents` | — | Agent selection, discovery, subagent monitoring |
| `/browser` | — | Open sandboxed Chrome browser |
| `/goal` | — | Run until task is completely finished without intermediate input |
| `/grill-me` | — | Before implementing, ask clarifying questions to align on plan details |
| `/schedule` | — | Run instruction as one-time timer or recurring schedule |

### Tools and Tasks `[DOCS]`

| Command | Alias | Description |
|---|---|---|
| `/codesearch` | `/cs`, `/search` | Interactive code search with regex and line commenting |
| `/hooks` | — | Browse active hooks |
| `/mcp` | — | Interactive MCP manager |
| `/permissions` | — | Fine-grained permissions editor |
| `/skills` | — | Browse loaded skills |
| `/tasks` | — | Task Manager Panel for background logs |

### Utilities `[DOCS]`

| Command | Alias | Description |
|---|---|---|
| `/add-dir` | — | Add working directory |
| `/artifact` | — | Open artifact picker |
| `/btw` | — | Provide additional context |
| `/clear` | — | Clear terminal history |
| `/context` | — | Inspect memory and token usage |
| `/copy` | — | Copy content to clipboard |
| `/diff` | — | Workspace diff viewer |
| `/open <path>` | — | Open in default editor |
| `/feedback` | — | Feedback submission |
| `/title` | — | Toggle/configure terminal titles |
| `/statusline` | — | Configure custom status line |

### Account `[DOCS]`

| Command | Alias | Description |
|---|---|---|
| `/credits` | — | Manage AI Premium credits |
| `/logout` | — | Disconnect, purge auth tokens |
| `/usage` | `/quota` | View model quota |

### Special Input `[DOCS]`

| Input | Description |
|---|---|
| `! <command>` | Direct bash execution (shell mode) |
| `@ <path>` | File autocompletion overlay |

### Binary Subcommands (verified hands-on 2026-08-11)

| Command | Description |
|---|---|
| `agy agents` / `agy agent` | List available agents (workspace + global + plugin-shipped) |
| `agy models` | List available models |
| `agy plugin` / `agy plugins` | Manage plugins: list, import, install, uninstall, enable, disable, validate, link |
| `agy changelog` | Show changelog and release notes |
| `agy install` | Configure environment paths and shell settings |
| `agy update` | Update CLI |

---

## 8. Built-in Agent Tool API

> [!NOTE]
> The official documentation lags the live CLI. While the official docs document only 18 tools, the live CLI exposes a complete set of **56 tools** (verified via the headless `stream-json` `init` event's `tools` array as of 2026-08-11).
> Tool argument signatures are only officially verified for the original 18 tools. The remaining 38 tools are verified by name, but their argument signatures are unverified (and thus no parameters are specified to avoid hallucinations).
> Description provenance follows the same rule: the 18 verified tools have descriptions sourced from official docs and observed transcripts; the 38 name-verified tools carry best-effort descriptions inferred from their tool names. The knowledge JSON flags this per tool (`args_verified`, `description_verified`) so agents can weigh each entry.

### File Operations (`file` family)

| Tool | Arguments | Args Verified | Description |
|---|---|---|---|
| `list_dir` | `DirectoryPath` (string) | Yes | List directory |
| `multi_replace_file_content` | `TargetFile` (string), `Instruction` (string), `Description` (string), `ReplacementChunks` (array), `TargetLintErrorIds` (array), `ArtifactMetadata` (object) | Yes | Multiple non-contiguous edits |
| `replace_file_content` | `TargetFile` (string), `Instruction` (string), `Description` (string), `AllowMultiple` (bool), `TargetContent` (string), `ReplacementContent` (string), `StartLine` (int), `EndLine` (int), `TargetLintErrorIds` (array) | Yes | Replace text block |
| `sed_file` | — | No | Perform regex replacements in a file |
| `view_file` | `AbsolutePath` (string), `StartLine` (int), `EndLine` (int), `ContentOffset` (int), `IsSkillFile` (bool) | Yes | Read file ranges |
| `write_to_file` | `TargetFile` (string), `Overwrite` (bool), `CodeContent` (string), `Description` (string), `IsArtifact` (bool), `ArtifactMetadata` (object) | Yes | Write files |

### Search and Research (`search` family)

| Tool | Arguments | Args Verified | Description |
|---|---|---|---|
| `find_by_name` | `SearchDirectory` (string), `Pattern` (string), `Type` (string), `Excludes` (array), `Extensions` (array), `FullPath` (bool), `MaxDepth` (int) | Yes | Glob search |
| `grep_search` | `SearchPath` (string), `Query` (string), `IsRegex` (bool), `CaseInsensitive` (bool), `Includes` (string), `MatchPerLine` (bool) | Yes | Text search |
| `search_web` | `query` (string), `domain` (string) | Yes | Web search |

### Execution and System (`execution` family)

| Tool | Arguments | Args Verified | Description |
|---|---|---|---|
| `call_mcp_tool` | `ServerName` (string), `ToolName` (string), `Arguments` (object) | Yes | Lazy MCP tool execution |
| `delete_knowledge` | — | No | Delete a knowledge file or memory entry |
| `generate_image` | — | No | Generate an image using the internal Nano Banana model |
| `read_url_content` | `URL` (string) | Yes | Fetch URL content |
| `run_command` | `CommandLine` (string), `Cwd` (string), `WaitMsBeforeAsync` (int), `RunPersistent` (bool), `RequestedTerminalID` (string) | Yes | Execute bash |

### Control and Safety (`control` family)

| Tool | Arguments | Args Verified | Description |
|---|---|---|---|
| `ask_permission` | `Action` (string), `Target` (string), `Reason` (string) | Yes | Request permissions |
| `ask_question` | — | No | Ask the user one or more multiple-choice questions |
| `command_status` | — | No | Check the status of a running background command |
| `finish` | — | No | Mark the current goal/task as successfully completed |
| `list_permissions` | (no args) | Yes | View current grants |
| `manage_task` | `Action` (`list`/`kill`/`status`/`send_input`), `TaskId` (string), `Input` (string) | Yes | Background task control |
| `schedule` | `DurationSeconds` (int), `CronExpression` (string), `MaxIterations` (int), `Prompt` (string), `TimerCondition` (string) | Yes | Timers and cron jobs |
| `send_command_input` | — | No | Send input text to a running background task |
| `wait` | — | No | Wait for a specified condition or duration |
| `wait_5_seconds` | — | No | Wait exactly 5 seconds |

### Agent Collaboration (`collaboration` family)

| Tool | Arguments | Args Verified | Description |
|---|---|---|---|
| `define_subagent` | (session-scoped) | Yes | Create transient subagent template |
| `invoke_subagent` | `Subagents` (array with `Prompt`, `Role`, workspace options) | Yes | Spawn subagent |
| `manage_inbox` | — | No | Manage user-queued messages and system notifications |
| `manage_subagents` | — | No | Manage background subagents |
| `send_message` | `Message` (string), `Recipient` (string) | Yes | Inter-agent / subagent messaging |

### Resources (`resources` family)

| Tool | Arguments | Args Verified | Description |
|---|---|---|---|
| `list_resources` | — | No | List resources exposed by loaded MCP servers |
| `read_resource` | — | No | Read contents of a loaded MCP resource |

### Notebooks (`notebook` family)

| Tool | Arguments | Args Verified | Description |
|---|---|---|---|
| `notebook_edit` | — | No | Edit code cells in a Jupyter notebook |
| `notebook_execution` | — | No | Execute cells in a Jupyter notebook |

### Browser Automation (`browser` family)

| Tool | Arguments | Args Verified | Description |
|---|---|---|---|
| `browser_click_element` | — | No | Click an element on the active browser page |
| `browser_drag_pixel_to_pixel` | — | No | Drag from one pixel coordinate to another |
| `browser_get_dom` | — | No | Retrieve the DOM structure of the active page |
| `browser_get_network_request` | — | No | Get detailed info for a specific network request |
| `browser_input` | — | No | Input text into a browser input field |
| `browser_list_network_requests` | — | No | List network requests captured for the active page |
| `browser_mouse_down` | — | No | Trigger a mouse down event at coordinates |
| `browser_mouse_up` | — | No | Trigger a mouse up event at coordinates |
| `browser_move_mouse` | — | No | Move the mouse to specific coordinates |
| `browser_press_key` | — | No | Press a key or key combination on the page |
| `browser_refresh_page` | — | No | Refresh the active browser page |
| `browser_resize_window` | — | No | Resize the browser window dimensions |
| `browser_scroll` | — | No | Scroll the browser window by an offset |
| `browser_scroll_dom` | — | No | Scroll a specific DOM element by selector |
| `browser_select_option` | — | No | Select an option from a dropdown element |
| `browser_subagent` | — | No | Invoke the browser subagent |
| `capture_browser_console_logs` | — | No | Retrieve console logs from the active page |
| `capture_browser_screenshot` | — | No | Take a screenshot of the active browser window |
| `click_browser_pixel` | — | No | Click specific pixel coordinates on the screen |
| `execute_browser_javascript` | — | No | Execute arbitrary JavaScript on the active page |
| `list_browser_pages` | — | No | List all active pages/tabs in the browser profile |
| `open_browser_url` | — | No | Open a URL in the browser profile |
| `read_browser_page` | — | No | Read text/HTML content of the active page |

---

## 9. Sandbox

`[DOCS]`

| Platform | Technology |
|---|---|
| Linux | `nsjail` |
| macOS | `sandbox-exec` |
| Windows | `AppContainer` |

Interactive behavior: bypass for single execution when enabled; force sandbox for single command when disabled.

---

## 10. Headless Mode

`[DOCS]` — Re-verified against live docs 2026-08-11 (previous version was based on a truncated page).

**Run flags:** `-p`, `--print`, `--prompt`

**Full flag reference:**

| Flag | Default | Description |
|---|---|---|
| `-p`, `--print`, `--prompt` | — | Run a single prompt non-interactively and print the response |
| `--output-format` | `text` | `text`, `json`, or `stream-json` |
| `--json-schema` | — | Schema string, `.json` file path, or primitive type name (`string`, `number`, `integer`, `boolean`) |
| `--model` | — | Model slug for the run (list with `agy models`) |
| `--effort` | — | Reasoning effort: `low`, `medium`, `high` |
| `--agent` | — | Agent for the run (list with `agy agents`) |
| `--continue`, `-c` | `false` | Continue the most recent conversation |
| `--conversation` | — | Resume a conversation by ID |
| `--dangerously-skip-permissions` | `false` | Auto-approve all tool permission requests |
| `--print-timeout` | `5m` | Maximum time to wait for a response |
| `--sandbox` | `false` | Run with terminal sandbox restrictions enabled |
| `--add-dir` | `[]` | Add a directory to the workspace (repeatable) |
| `--disable-slash-commands` | `false` | Disable slash command and skill expansion in print mode |
| `--log-file` | — | Override CLI log file path |
| `--mode` | — | Agent execution mode: `accept-edits`, `plan` |
| `--prompt-interactive`, `-i` | — | Run an initial prompt interactively and continue the session |

**Status enum (complete, re-verified):**

| Status | Meaning |
|---|---|
| `SUCCESS` | Run completed and produced a response |
| `ERROR` | Run ended with an error |
| `CANCELED` | Run was canceled |
| `INTERRUPTED` | Run was interrupted (e.g., SIGINT) |
| `INVALID` | Run reached an invalid state |
| `WAITING` | Run ended while waiting on input |
| `RUNNING` | Run did not reach a terminal state |

**Exit codes:** `0` on success; non-zero when no response is produced (reason written to stderr). In `json`/`stream-json` modes, failures also surface in the `status` and `error` fields. Pinning an unknown `--model` exits non-zero with `ERROR` — no silent fallback.

**Note on `--agent` (verified hands-on 2026-08-11):** unlike `--model`, `--agent` does **not** reject unknown names in headless mode — a run with `--agent definitely-not-an-agent` succeeds silently with the default agent. Custom agents (including plugin-shipped ones) are discoverable via `agy agents`. Headless loading of **workspace-scoped** custom agents was **MEASURED 2026-08-11 and does not occur**: a fixture workspace's plugin agent (`marker-agent`) and plain workspace agent (`workspace-control`) both returned the default agent's generic reply under `-p --agent <name>` — their marker system prompts never fired, and unknown names fall back silently too. Global plugin agents (e.g. `self-auditor`) are the only custom agents confirmed to load (interactive session, transcript `a1e51ef2`). Note the surface split: the interactive TUI `/agents` selector **does** list workspace-scoped agents (user-verified 2026-08-11); only headless `--agent` and `agy agents` ignore them.

**JSON Envelope (`--output-format json`):**

| Field | Type | Presence |
|---|---|---|
| `conversation_id` | string | Always |
| `status` | string | Always (see status enum) |
| `response` | string | Always |
| `error` | string | Failure only |
| `duration_seconds` | number | Always |
| `num_turns` | number | Always |
| `structured_output` | object | With `--json-schema` only |
| `json_schema` | object | With `--json-schema` only |
| `usage` | object | `input_tokens`, `output_tokens`, `thinking_tokens`, `cache_read_tokens`, `total_tokens` |

**Streaming (`--output-format stream-json`):** Newline-delimited JSON (NDJSON) events: `init` (once), `step_update` (per step transition or text delta), `result` (once, same shape as `json`). `step_update` payloads carry `state` (`ACTIVE`/`DONE`), `step_type` (`user_input`, `agent_response`, `tool`, `checkpoint`), `tool_name`, `text_delta`, `usage`, `tool_info` (`name`, `parameters`, `output`, `error{type,message}`), and `subagent_info` (`subagents` with `type_name`, `role`, `conversation_id`, `log_uri`, `workspace_uris`). The `init` payload records `cwd`, `tools`, `permission_mode` (`request-review` default; `always-proceed` under `--dangerously-skip-permissions`), and optional `model`/`agent`/`json_schema`.

**Permissions in headless:** No interactive prompts exist. Tools requiring approval are soft-denied: the run continues, exits `0`, and prints a stderr notice naming the tool. Pre-grant via `permissions.allow` rules in `~/.gemini/antigravity-cli/settings.json`, or auto-approve with `--dangerously-skip-permissions`. Workspace reads/writes are auto-allowed.

**Subcommands:** `agy models` lists model slugs (e.g., `gemini-3.6-flash-high`, `gemini-3.6-flash-medium`, `gemini-3.5-flash-medium`, `gemini-3.1-pro-high`, `claude-sonnet-4-6`); `agy agents` lists available agents (global + workspace + plugin-shipped); `agy plugin` manages plugins; see Section 7 for the full subcommand inventory. Note: `agy models` and `agy agents` can hang in some contexts (observed 2026-08-11) — likely awaiting a network call.

**Authentication:** Cached credentials required. Non-interactive environments without cached credentials get `authentication required` error.

**Project flag:** `--project=<project_id>` combinable with headless mode.

---

## 11. Browser Integration

`[DOCS]`

| Aspect | Detail |
|---|---|
| Engine | Local Chrome, separate profile |
| Isolation | No cookie/sign-in sharing with personal browsing |
| Sign-in persistence | Persists within isolated profile |
| macOS | Separate dock icon if Chrome is open |
| Disable | "Browser Tools" in User Settings |
| Security | Denylist (Google BadUrlsChecker, server-side) + Allowlist (local file, starts with localhost) |
| Precedence | Denylist always wins |
| Invocation | `/browser` command |

**Design rationale:** `/browser` is a separate command rather than auto-invoked because user feedback indicated the agent was not capable enough to determine when to use the browser `[DOCS]`.

---

## 12. Artifacts and Implementation Plans

`[DOCS]`

**Execution Modes:**

| Mode | Behavior | CLI |
|---|---|---|
| Planning | Agent plans, produces artifacts, task groups | `/planning` |
| Fast | Direct execution | `/fast` |

**Artifacts:** Implementation plans, code diffs, architecture diagrams, images, browser recordings.

**Controls:** `Ctrl+R` or `/artifact` for picker. `y`/`n`/`Shift+A`/`Shift+R` for approval. `p` for preview.

**Review Policy (Desktop):**

| Policy | Behavior |
|---|---|
| Request Review (Recommended) | Agent halts for approval |
| Always Proceed | Never halts |

**Implementation Plan Workflow:** Generate → Review (inline comments) → "Proceed" or "Review" → Agent iterates or implements.

**Multimodal Feedback:** Screenshots via browser subagent, saved as artifacts, support commenting.

---

## 13. Enterprise Features

`[DOCS]`

**Editions:** Standard, Plus, Pay-as-you-go.

**Authentication:**

| Method | Details |
|---|---|
| Standard SSO | Google account |
| BYOID | Workforce Identity Federation (Okta, Ping, etc.) |
| ADC | `gcloud auth application-default login`. Credentials at `~/.config/gcloud/application_default_credentials.json` |

**Diagnostic Logs:**

| Product | Path |
|---|---|
| CLI | `~/.gemini/antigravity-cli/cli.log` |
| Desktop | `~/Library/Logs/Antigravity/language_server.log` |

**Regional Endpoints:** Global (full features), US, EU (no Image Generation).

**Projects:** Default `default-cli-project`. `--project=<id>`, `--new-project`. Cross-project `/fork`.

**Conversations:** Workspace-scoped. Prevents context pollution.

**Desktop Workflows:**
- **Project creation:** Multi-folder, cross-repository context support
- **Agent startup:** Local Mode (direct in folders) or New Worktree Mode (isolated git worktree)

---

## 14. Workspace Governance Recommendations

These are engineering recommendations grounded in confirmed system behavior but not documented as official guidance.

### 14.1 Plugin-Based Governance

`[DOCS]` confirms native `disable`/`enable` for plugins. Package related skills into plugins for native toggle `[B]`.

### 14.2 Archive-Based Skill Indexing

Move non-essential skills to `./skills_archive/`. Use routing skill for on-demand loading. Reduces Phase 1 token overhead `[B]`.

### 14.3 Workspace Shadowing

Workspace skills override global skills with identical names. Create workspace skill to redirect global skill `[B]`.

### 14.4 Version-Controlled Settings

Commit workspace settings to enforce security policies across teams `[A]`.

---

## 15. Complete Path Inventory

### CLI Paths `[DOCS]`

| Path | Purpose |
|---|---|
| `~/.gemini/antigravity-cli/settings.json` | User preferences |
| `~/.gemini/antigravity-cli/keybindings.json` | Keybinding overrides |
| `~/.gemini/antigravity-cli/cache/last_conversations.json` | Session cache |
| `~/.gemini/antigravity-cli/cli.log` | Diagnostic log |
| `~/.gemini/antigravity-cli/updater/update.lock` | Self-updater advisory lock |
| `~/.gemini/antigravity-cli/updater/last_check.timestamp` | Self-updater 15-min TTL debounce marker |
| `~/.gemini/antigravity-cli/statusline.sh` | Example status line script path (per official statusline docs) |

**Conversation data (verified hands-on 2026-08-11):**

| Path | Purpose |
|---|---|
| `~/.gemini/antigravity-cli/brain/<conversation_id>/.system_generated/logs/transcript.jsonl` | Conversation transcript (JSONL; schema in §18.1) |
| `~/.gemini/antigravity-cli/brain/<conversation_id>/.system_generated/logs/transcript_full.jsonl` | Full transcript (native-typed tool args) |
| `~/.gemini/antigravity-cli/brain/<conversation_id>/scratch/` | Scratch directory |
| `~/.gemini/antigravity-cli/brain/<conversation_id>/.user_uploaded/` | User-uploaded files |
| `~/.gemini/antigravity-cli/conversations/<conversation_id>.db` | Conversation store (SQLite; `-shm`/`-wal` sidecars) |
| `~/.gemini/antigravity-cli/presence/<conversation_id>.lock` | Presence lock |
| `~/.gemini/tmp/ctx_<conversation_id>.json` | Context temp file |

Auto-update can be disabled with the `AGY_CLI_DISABLE_AUTO_UPDATE=true` environment variable `[DOCS]`.

### Global Configuration `[DOCS]`

| Path | Purpose |
|---|---|
| `~/.gemini/config/skills/<name>/SKILL.md` | Global skills |
| `~/.gemini/config/mcp_config.json` | Global MCP servers |
| `~/.gemini/config/hooks.json` | Global hooks |
| `~/.gemini/config/plugins/<name>/` | Global plugins |
| `~/.gemini/config/agents/<name>.md` | Global agents |
| `~/.gemini/GEMINI.md` | Global context rules |

### Workspace `[DOCS]`

| Path | Purpose |
|---|---|
| `.agents/skills/<name>/SKILL.md` | Workspace skills |
| `.agents/mcp_config.json` | Workspace MCP servers |
| `.agents/hooks.json` | Workspace hooks |
| `.agents/plugins/<name>/` | Workspace plugins |
| `.agents/agents/<name>.md` | Workspace agents |
| `.agents/rules/` | Workspace rules |
| `GEMINI.md` | Workspace context rules |
| `AGENTS.md` | Workspace agent rules |

### Application `[DOCS]`

| Path | Purpose |
|---|---|
| `~/.gemini/antigravity/` | Desktop app data (CLI also references this tree for shared state) |
| `~/.gemini/antigravity/mcp_oauth_tokens.json` | OAuth tokens |
| `~/.gemini/antigravity/brain/...` | Desktop brain. **Note:** the official CLI statusline example shows this path, but the CLI's real transcript path (verified 2026-08-11) is `~/.gemini/antigravity-cli/brain/...` — the docs example is stale. |

### System `[GOOGLE]`

| Path | Purpose |
|---|---|
| `/etc/gemini-cli/system-defaults.json` | System defaults (Linux) |
| `C:\ProgramData\gemini-cli\system-defaults.json` | System defaults (Windows) |
| `/Library/Application Support/GeminiCli/system-defaults.json` | System defaults (macOS) |
| `/etc/gemini-cli/settings.json` | System settings (Linux) |
| `C:\ProgramData\gemini-cli\settings.json` | System settings (Windows) |
| `/Library/Application Support/GeminiCli/settings.json` | System settings (macOS) |
| `~/.config/gcloud/application_default_credentials.json` | Google ADC |

### Install Paths `[DOCS]`

| Path | Platform |
|---|---|
| `~/.local/bin` | macOS/Linux |
| `C:\Users\<Username>\AppData\Local\agy\bin` | Windows (binary) |
| `C:\Program Files\Google\antigravity-cli` | Windows (PATH entry per troubleshooting docs) |

---

## 16. Information Sourced Outside Official Docs

This section explicitly catalogs every piece of information in this report that comes from sources other than `antigravity.google/docs/*`. Each entry identifies the source category, specific source, what it contributed, and why it was included.

### From Google-Owned, Non-Antigravity Sources `[GOOGLE]`

| Information | Source | Why Included |
|---|---|---|
| Written in Go, Gemini 3.5 Flash optimized | Codelab: Getting Started `[GOOGLE]` | Not stated on official docs pages |
| Progressive disclosure token costs (~100/skill Phase 1, <5000 Phase 2) | Codelab: Skills 101 `[GOOGLE]` | Official docs describe pattern but omit quantitative details |
| `scripts/`, `references/`, `assets/` subdirectories (Codelab names) | Codelab: Skills 101 `[GOOGLE]` | Superseded by official docs page which uses `scripts/`, `examples/`, `resources/` |
| 7-level configuration precedence | Gemini CLI Configuration docs `[GOOGLE]` | Not stated in Antigravity docs; likely inherited but unconfirmed |
| Environment variable interpolation syntax | Gemini CLI docs `[GOOGLE]` | Not mentioned in Antigravity docs |
| `general.preferredEditor` 18 enum values | Gemini CLI docs `[GOOGLE]` | Not in Antigravity docs |
| `general.openEditorInNewWindow`, `general.vimMode` | Gemini CLI docs `[GOOGLE]` | Not in Antigravity docs |
| `policyPaths`, `adminPolicyPaths` | Gemini CLI docs `[GOOGLE]` | Not in Antigravity docs |
| Migration path mapping (`~/.gemini/skills/` → `~/.gemini/config/skills/`) | Migration docs `[GOOGLE]` | Provides critical path correction for users migrating from Gemini CLI |
| `AfterAgent`/`AfterTool` event names | Claude-Mem integration docs `[COMMUNITY]` | Official hooks docs list `PreInvocation`/`PostInvocation`; naming discrepancy unresolved |
| Nano Banana 2 model for image generation | LinkedIn blog post `[GOOGLE]` | Not mentioned in official docs |
| `/goal` command and subagent loop patterns | LinkedIn blog post `[GOOGLE]` | `/goal` now confirmed on official landing page; loop patterns are user experience |
| `serverUrl` replaces legacy `url`/`httpUrl` | Migration docs `[GOOGLE]` | Critical migration detail |

### From Third-Party Sources `[COMMUNITY]`

| Information | Source | Why Included |
|---|---|---|
| Skills interoperable across Claude Code, Cursor, Codex CLI | OrangeBot `[COMMUNITY]`, GitHub (claude-faces-expert) `[COMMUNITY]` | Official docs don't explicitly state cross-tool portability of Skills |
| Security: hidden Unicode instructions can survive human review | Embrace The Red `[COMMUNITY]` | Official docs don't address this security concern |
| `disable-model-invocation` frontmatter attribute | Embrace The Red `[COMMUNITY]` | Not in official docs; may not exist — included only as security concern reference |
| 30-day usage patterns, `/goal` command usage | LinkedIn `[COMMUNITY]` | First-person user experience with CLI |

---

## 17. Undocumented Behavioral Contracts

The official docs (`antigravity.google/docs/*`) leave the following behavioral questions unanswered. These represent gaps in the behavioral specification — not necessarily missing features, but missing documentation about how features behave.

### Configuration Behavioral Gaps

| Question | Context | Impact |
|---|---|---|
| What does `commandExecutionPolicy: "eager"` do vs `auto` vs `sandbox` vs `off`? | Agent frontmatter lists 4 values but defines none | Developers cannot choose between policies without testing |
| What does `artifactReviewPolicy: "agent-decides"` trigger on? | Listed as valid option in settings | Unpredictable review behavior in production |
| What does `runningLightSpeed: "fast"` change vs `medium`/`slow`/`off`? | All 4 values listed in settings | Users cannot meaningfully configure rendering speed |
| What counts as a "read" tool for `toolPermission: "strict"`? | `strict` prompts for "all non-read tools" | Is `grep_search` a read? Is `list_dir` a read? Is `search_web` a read? |
| What happens when `enableTerminalSandbox: true` and the OS sandbox technology is unavailable? | Three technologies listed but fallback behavior undocumented | Potential silent security gap |

### Extensibility Behavioral Gaps

| Question | Context | Impact |
|---|---|---|
| What glob syntax do Rules use in `Glob` activation mode? | Official docs mention "Glob" mode | Incorrect patterns could silently fail to match |
| How does `model: inherit` resolve — parent's selected model or parent's default? | Agent frontmatter `model` field | Subagent may use wrong model tier |
| What happens when two workspace skills share the same name? | Workspace > Global precedence stated; same-level conflicts not | Unpredictable skill activation |
| What is the plugin loading order when multiple plugins define hooks for the same event? | Multiple plugins can include hooks.json | Non-deterministic hook execution order |
| Does a disabled MCP server still appear in `/mcp`? Still count against startup? | `disabled` config field exists | UX confusion |
| What happens when a hook exceeds its `timeout` value? | `timeout` field documented; behavior on timeout is not | Silent failures could bypass safety hooks |
| What happens when a `tools` list in agent frontmatter contains a misspelled tool name? | Documented as known issue causing hang; no validation fallback described | Subagent hangs indefinitely |
| What is the MCP server connection failure behavior? Does the session fail or degrade gracefully? | Not addressed | Potential session failures in production |
| Can a Running subagent transition directly to Killed, or must it pass through Idle? | Three states documented; transition rules are not | State machine behavior unclear |
| What happens when `mainAgent: false` and `subagent: false`? | Both fields documented | Is the agent unusable? Hidden? |

### Headless Mode Gaps

*Both gaps below resolved 2026-08-11 (see Section 10).*

| Question | Resolution |
|---|---|
| What are all valid `status` enum values in JSON output? | `SUCCESS`, `ERROR`, `CANCELED`, `INTERRUPTED`, `INVALID`, `WAITING`, `RUNNING` |
| What is the exit code mapping? | `0` = success; non-zero = no response produced (reason on stderr) |

### CLI Subcommand Behavior Gaps

| Question | Context | Impact |
|---|---|---|
| Why do `agy agents` / `agy models` appear to hang? | Both subcommands perform a remote fetch with **no visible client-side timeout** (observed 2026-08-11: ~8 s on a healthy network; still pending after 45 s inside a restricted/sandboxed network such as the Freebuff tool environment). Neither has an offline/JSON mode (`agy agents --output-format json` errors). | Automation that shells out to these commands must impose its own timeout; don't treat a slow run as a bug |
| Why don't workspace-scoped agents show up in headless mode but do in the TUI? | `.agents/agents/` and `.agents/plugins/<name>/agents/` agents are **not** listed by `agy agents` and are **not** loaded by headless `-p --agent` (any unresolvable name silently falls back to the default agent) — but the interactive TUI `/agents` selector **does** list them (user-verified 2026-08-11). | Discovery behavior differs by surface: headless/CLI = global + plugin agents only; interactive TUI = also workspace agents. Pinning a workspace agent in headless automation will silently use the default agent instead |

### Sandbox Gaps

| Question | Context | Impact |
|---|---|---|
| What specific network restrictions does each sandbox technology impose? | Technology names given (nsjail, sandbox-exec, AppContainer) but restriction details are not | Security teams cannot assess the security boundary |
| What filesystem restrictions does each sandbox impose? | Same as above | Same as above |
| Is sandbox behavior identical across all three platforms? | Three different technologies | Cross-platform parity unknown |

### Permissions Gaps

| Question | Context | Impact |
|---|---|---|
| What happens when a permission rule matches multiple lists with conflicting actions? | Deny > Ask > Allow stated, but edge cases with glob patterns undocumented | Potential unexpected permission behavior |
| How do cross-platform path normalizations handle symlinks? | Path normalization confirmed; symlink handling not | Security boundary could be circumvented |

---

## 18. Remaining Hard Gaps

These are specific pieces of information that no source — official, Google-owned, or community — has provided:

| Gap | Status | Impact | How to Resolve |
|---|---|---|---|
| **`transcript.jsonl` field-level schema** | **RESOLVED 2026-08-11 (hands-on):** full line schema captured from live `agy` 1.1.11 sessions; see §18.1. Transcripts confirmed at `~/.gemini/antigravity-cli/brain/<conversation_id>/.system_generated/logs/transcript.jsonl` (+ `transcript_full.jsonl`). | No longer a blocker. | — |
| **Headless mode `status` enum values** | **RESOLVED 2026-08-11:** `SUCCESS`, `ERROR`, `CANCELED`, `INTERRUPTED`, `INVALID`, `WAITING`, `RUNNING`. Exit codes also documented: `0` success, non-zero failure. | No longer a blocker. | — |
| **`general.defaultApprovalMode` enum values** | **RESOLVED 2026-08-11:** `default`, `auto_edit`, `plan` (default: `default`). Docs relocated to `geminicli.com`; old `google.github.io` URL 404s. | Minor migration impact. | — |
| **Plugin `agents/` subdirectory** | **RESOLVED 2026-08-11 (hands-on) for the global path:** plugins DO support `agents/` (and `commands`) components — `agy plugin list` reports `agents` on installed plugins (`self-customizer` ships `agents/self-auditor.md`), `agy agents` lists `self-auditor`, and the `self-auditor` transcript proves execution. The plugins docs page directory structure is incomplete. **Workspace-scoped `.agents/plugins/` agents (MEASURED 2026-08-11): surfaced only in the interactive TUI** — not listed by `agy agents`, not loaded by headless `--agent` (silent fallback), not tracked by `agy plugin list`; but the TUI `/agents` selector lists them (user-verified). See §4.4 and §17. | Global path: no longer a blocker. Workspace path: TUI = works; headless/CLI = not surfaced (silent fallback). | Fixture: `tests/fixtures/plugin-workspace/` |
| **CLI brain directory path** | **RESOLVED 2026-08-11 (hands-on):** actual CLI path is `~/.gemini/antigravity-cli/brain/<conversation_id>/`. The docs' statusline example (`~/.gemini/antigravity/brain/`) is stale — it mirrors the desktop path. | No longer a blocker. | — |

---

## 18.1 Transcript Schema — Verified Hands-On (2026-08-11)

Source: live `agy` 1.1.11 sessions — 2 headless probes plus an interactive `self-auditor` agent run (72 entries, 40 tool calls across view_file/list_dir/find_by_name/grep_search/run_command). Enum completeness further verified by a full-brain audit (2026-08-11): **49,586 lines across 33 sessions** scanned with `scripts/audit_transcripts.py`; evidence at `audits/transcript-audit-2026-08-10.json` in the reference repo. Files confirmed at:

- `~/.gemini/antigravity-cli/brain/<conversation_id>/.system_generated/logs/transcript.jsonl`
- `~/.gemini/antigravity-cli/brain/<conversation_id>/.system_generated/logs/transcript_full.jsonl`

Both files share the same line schema. Difference observed: `transcript_full.jsonl` stores tool-call args as native JSON values; `transcript.jsonl` stores them as escaped strings.

**Line schema (one JSON object per line):**

| Field | Type | Presence | Notes |
|---|---|---|---|
| `step_index` | int | Always | Zero-based step order |
| `source` | enum | Always | `USER_EXPLICIT`, `SYSTEM`, `MODEL` — complete (audit confirmed no others) |
| `type` | enum | Always | 10 originally verified + 9 promoted by full-brain audit (2026-08-11): `USER_INPUT`, `CONVERSATION_HISTORY`, `PLANNER_RESPONSE`, `CHECKPOINT`, `ERROR_MESSAGE`, `VIEW_FILE`, `LIST_DIRECTORY`, `FIND`, `GREP_SEARCH`, `RUN_COMMAND`, `ASK_QUESTION`, `CODE_ACTION`, `EPHEMERAL_MESSAGE`, `GENERIC`, `INVOKE_SUBAGENT`, `MCP_TOOL`, `READ_URL_CONTENT`, `SEARCH_WEB`, `SYSTEM_MESSAGE`. Tool entries use the SCREAMING_SNAKE tool name; `CODE_ACTION` (3,756×) and `ASK_QUESTION` (225×) are the most common non-doc values |
| `status` | enum | Always | `DONE` (49,070×), `RUNNING` (408×, in-progress/background steps), `ERROR` (108×, failed steps) — complete per audit; the earlier `ACTIVE` guess is superseded |
| `created_at` | string | Always | ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`) |
| `content` | string | Optional | `USER_INPUT`: prompt wrapped in `<USER_REQUEST>`/`<ADDITIONAL_METADATA>`/`<USER_SETTINGS_CHANGE>` tags; `PLANNER_RESPONSE`: model reply; `RUN_COMMAND`: command output; `CHECKPOINT`: truncation summary with `{{ CHECKPOINT N }}` marker |
| `thinking` | string | Optional | Model reasoning; observed on `PLANNER_RESPONSE` |
| `tool_calls` | array | Optional | Tools invoked on `PLANNER_RESPONSE`. Each: `{name, args}`; `args` are tool-specific (e.g. `CommandLine`, `Cwd`, `WaitMsBeforeAsync`, `toolAction`, `toolSummary` for `run_command`) |
| `exit_code` | int | Optional | Observed on `RUN_COMMAND` |

**Implications for tooling:**

- The `created_at` field is UTC, but tool-output `content` opens with a `Created At`/`Completed At` header in LOCAL time (with offset) — parse accordingly.
- `conversation_id` is **not** stored in the file — derive it from the directory name.
- Checkpoint entries embed absolute paths to the log files.
- `step_index` is not necessarily contiguous: one `PLANNER_RESPONSE` may issue multiple `tool_calls`, leaving gaps between entries.
- Tool entries expose their args in `PLANNER_RESPONSE.tool_calls` — each `{name, args}` where args carry tool-specific fields (e.g. `AbsolutePath` for view_file, `DirectoryPath` for list_dir, `CommandLine`/`Cwd`/`WaitMsBeforeAsync` for run_command) plus metadata fields `toolAction` and `toolSummary`.
- `ERROR_MESSAGE` entries (source `SYSTEM`) embed the failure text with `Guidance` and `Retries remaining: N`; they carry no `exit_code`.
- `status` distinguishes lifecycle: `RUNNING` marks in-progress steps (e.g. background `RUN_COMMAND` with task id), `ERROR` marks failed steps, `DONE` marks completion.
- `MCP_TOOL` entries carry MCP tool output (e.g. `Found 3 collections`); `ASK_QUESTION` entries embed the user's answers (`A1: ...`) in `content`; `INVOKE_SUBAGENT` entries embed subagent creation JSON.
- `LIST_DIRECTORY` output is JSON-lines: `{"name": ..., "sizeBytes": ...}` per entry.
- In the headless probe run, `RUN_COMMAND` executed with `Cwd` = `~/.gemini/antigravity-cli` (the CLI config dir) rather than the invocation directory — an interactive run used the correct workspace cwd, so this looks headless-specific; verify before relying on cwd in automation.

## 19. Works Cited

All sources are tagged by category: `[DOCS]` = official docs, `[GOOGLE]` = other Google sources, `[PROTOCOL]` = MCP specification, `[COMMUNITY]` = third-party.

### Official Docs `[DOCS]`

1. Hooks — https://antigravity.google/docs/hooks
2. MCP — https://antigravity.google/docs/mcp
3. Settings — https://antigravity.google/docs/cli/settings
4. CLI Reference — https://antigravity.google/docs/cli/reference
5. Subagents — https://antigravity.google/docs/subagents
6. Sandbox — https://antigravity.google/docs/cli/sandbox
7. Permissions — https://antigravity.google/docs/cli/permissions
8. Skills — https://antigravity.google/docs/skills
9. Plugins — https://antigravity.google/docs/plugins
10. Headless Mode — https://antigravity.google/docs/cli/headless
11. Projects — https://antigravity.google/docs/cli/projects
12. Conversations — https://antigravity.google/docs/cli/conversations
13. Artifacts — https://antigravity.google/docs/cli/artifacts
14. Status Line — https://antigravity.google/docs/cli/statusline
15. Title — https://antigravity.google/docs/cli/title
16. Troubleshooting — https://antigravity.google/docs/cli/troubleshooting
17. Best Practices — https://antigravity.google/docs/cli/best-practices
18. Enterprise — https://antigravity.google/docs/enterprise
19. Models — https://antigravity.google/docs/models
20. Rules & Workflows — https://antigravity.google/docs/rules-workflows
21. Agent Settings — https://antigravity.google/docs/agent-settings
22. Artifact Review — https://antigravity.google/docs/artifact-review
23. Browser — https://antigravity.google/docs/ide/browser
24. Allowlist / Denylist — https://antigravity.google/docs/ide/allowlist-denylist
25. Agent Side Panel — https://antigravity.google/docs/ide/agent-side-panel
26. Separate Chrome Profile — https://antigravity.google/docs/ide/separate-chrome-profile
27. Screenshots — https://antigravity.google/docs/screenshots
28. Implementation Plan — https://antigravity.google/docs/implementation-plan
29. Landing Page — https://antigravity.google/docs/

### Google-Owned, Non-Docs `[GOOGLE]`

30. Agent Skills 101 — https://codelabs.developers.google.com/getting-started-with-antigravity-skills
31. Getting Started with Google Antigravity — https://codelabs.developers.google.com/getting-started-google-antigravity
32. Spec-Driven Development — https://codelabs.developers.google.com/sdd-agy-cli
33. Hands-on with Antigravity CLI — https://codelabs.developers.google.com/antigravity-cli-hands-on
34. MCP servers with Gemini CLI — https://ai.google.dev/gemini-api/docs/mcp
35. Configuration — https://geminicli.com/docs/reference/configuration/ (relocated; old `google.github.io/gemini-cli/docs/configuration` returns 404 as of 2026-08-11)
36. Deprecation Notice — https://cloud.google.com/gemini/docs/codeassist/deprecation

### Protocol Specification `[PROTOCOL]`

37. MCP Specification — https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro

### Third-Party Sources `[COMMUNITY]`

38. Antigravity CLI Setup — https://docs.claude-mem.ai/antigravity-cli/setup
39. 30 Days of Antigravity CLI — https://www.linkedin.com/pulse/30-days-using-antigravity-cli
40. Scary Agent Skills — https://embracethered.com/blog/posts/2026/scary-agent-skills/
41. SKILL.md, explained — https://hiddedesmet.com/skills-md-github-copilot
42. Awesome Antigravity Skills — https://orangebot.ai/skills/antigravity
43. Build Custom Commands — https://dev.to/volodymyr_nehir/how-to-build-custom-commands-for-gemini-cli-and-antigravity-49mb
44. claude-faces-expert — https://github.com/omnifaces/claude-faces-expert
45. Auto Skill Usage — https://www.reddit.com/r/google_antigravity/comments/1vfxmh4/auto_skill_usage/
46. Google Antigravity Complete Guide — https://www.aibuilderclub.com/blog/google-antigravity-complete-guide
47. Antigravity CLI for AI Code Assistance — https://realpython.com/antigravity-cli/
48. Antigravity CLI — https://learn.arm.com/install-guides/antigravity/
49. Claude Code Components — https://ocdevel.com/mlg/mla-23
50. Claude Code SDK — https://skywork.ai/blog/claude-code-sdk-command-list-latest-reference/
51. AI Coding Tools Changelog — https://www.gradually.ai/en/changelogs/
52. ai-r MCP Server — https://glama.ai/mcp/servers/pro-target/ai-r

---

*End of Report — Version 5.1*
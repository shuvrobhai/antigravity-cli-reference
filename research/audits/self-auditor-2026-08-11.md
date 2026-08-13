# Self-Auditor Configuration Report — 2026-08-11

**Source transcript:** conversation `a1e51ef2-83a5-4440-9432-f34ec1e4733c` (`~/.gemini/antigravity-cli/brain/a1e51ef2-.../.system_generated/logs/transcript_full.jsonl`, 122 entries) — the `self-auditor` agent (shipped by the `self-customizer` plugin) ran a read-only audit of the `antigravity-cli` customization surfaces at **2026-08-11 02:52–02:56 (+06:00)**.

**Method:** (1) findings extracted from the agent's tool outputs and its final report (entry `[48]`); (2) every finding re-verified against the **live config** at 2026-08-11 ~11:00 (+06:00); (3) nothing was changed — this report is advisory only.

**Evidence citation format:** `[n]` = entry *n* of `transcript_full.jsonl` (0-indexed); quoted file lines refer to the numbered output embedded in that entry.

---

## 1. Audited Surface

| # | Surface | Status (audit) | Live (now) |
|---|---|---|---|
| 1 | Settings (`~/.gemini/antigravity-cli/settings.json`) | Configured | Configured |
| 2 | Plugins | 15 installed | 15 installed |
| 3 | Global skills (`~/.gemini/antigravity-cli/skills/`, `~/.gemini/config/skills/`) | 62 + 28 | 61 + 83 items |
| 4 | Workspace skills (`.agents/skills/`) | Not configured | Not configured (repo-level) |
| 5 | Rules (`~/.gemini/GEMINI.md`, `antigravity-cli/rules/global.md`) | Configured | Configured |
| 6 | MCP servers (`~/.gemini/config/mcp_config.json`) | 2 (`pieces`, `sequential-thinking`) | 2 |
| 7 | Hooks (plugin + trusted + statusline) | Configured | Configured |
| 8 | Subagents (global + plugin agents) | 3 | 3 |
| 9 | Keybindings (`keybindings.json`) | **Missing** (defaults in effect) | **Still missing** |
| 10 | Sandbox (`enableTerminalSandbox`) | **Not enabled** | **Still not enabled** |

---

## 2. Findings Summary

| ID | Finding | Severity | Evidence | Status (live) |
|---|---|---|---|---|
| F1 | `toolPermission: "always-proceed"` — no confirmation prompts for any tool | 🔴 HIGH | `[48]` §1; settings line 69 | **Confirmed** |
| F2 | `allowNonWorkspaceAccess: true` — agent may touch files outside the workspace | 🔴 HIGH | `[48]` §1; settings line 2 | **Confirmed** |
| F3 | `enableTerminalSandbox` unset → terminal commands run unsandboxed by default | 🟠 MEDIUM | `[48]` §1, §10 | **Confirmed** |
| F4 | `trustedWorkspaces` trusts 68 (now **95**) paths, including `~`, `~/Downloads`, `~/developer`, `~/Developer` — trust boundary ≈ whole home directory | 🟠 MEDIUM | `[1]` settings lines 70–138 | **Confirmed, grew** |
| F5 | 35 (now **44**) `permissions.allow` rules, mostly `unsandboxed(...)` shell utilities (`agy`, `find`, `cat`, `ls`, `grep`, `wc`, `git`, `pip install`, `python3`) | 🟠 MEDIUM | `[1]` settings lines 7–52 | **Confirmed, grew** |
| F6 | `permissions.deny` only 3 rules (`rm -rf /`, `wget`, one `read_file`) — no `curl`, `osascript`, or `curl \| sh` guard | 🟡 LOW | `[1]` settings lines 54–58 | **Confirmed** |
| F7 | `keybindings.json` missing — first read attempt failed with a tool-call error + retry guidance | ⚪ INFO | `[11]` (ERROR_MESSAGE) | **Confirmed** |
| F8 | Configured model `Gemini 3.5 Flash (Low)` differs from the session-selected `Gemini 3.6 Flash (High)` | ⚪ INFO | `[0]` USER_SETTINGS_CHANGE; settings line 5 | **Confirmed** |
| F9 | Custom hooks execute on every run: `self-customizer` (PreToolUse/PostToolUse), `i-have-adhd` (SessionStart), statusline script (37 KB), 2 `trusted_hooks.json` files | ⚪ INFO | `[15]`, `[48]` §7 | **Confirmed** |
| F10 | 15 plugins (8 claude-code, 6 antigravity, 1 gemini-cli); 7 claude-code imports ship `mcpServers` components; `sequential-thinking` runs via `npx -y` | ⚪ INFO | `[2]`, `[9]`, `[48]` §2, §6 | **Confirmed** |

**Bottom line:** nothing in the audit is wrong, and nothing has been silently fixed since — every finding still holds, and two surfaces (allow rules, trusted workspaces) have grown more permissive.

---

## 3. Detailed Findings

### F1 · `toolPermission: "always-proceed"` — 🔴 HIGH

- **What:** Every permitted tool runs **without any confirmation prompt** (settings.json `toolPermission`, line 69).
- **Evidence:** `[48]` §1: *"all permitted tools execute without interactive confirmation prompts"*; settings line 69 (`[1]`).
- **Why it matters:** The default is `request-review`. `always-proceed` removes the human checkpoint for write/bash/web tools — combined with F2–F5, an agent can act across your whole home directory with zero ask.
- **Live check:** still `"always-proceed"`.
- **Recommendation:** Switch to `"toolPermission": "request-review"` (default) or `"proceed-in-sandbox"` and let the fine-grained `permissions.allow` list be the fast-path.

### F2 · `allowNonWorkspaceAccess: true` — 🔴 HIGH

- **What:** File read/write is allowed **outside** the current workspace (settings line 2).
- **Evidence:** `[48]` §1 lists it as a non-default value; settings line 2 (`[1]`).
- **Why it matters:** The default is `false` (agent limited to project folders + `~/.gemini/antigravity/`). With `true`, nothing constrains the agent to your project.
- **Live check:** still `true`.
- **Recommendation:** Set to `false`. Most of the `trustedWorkspaces` entries exist precisely because this flag was on — turning it off and trusting only the workspaces you actually work in is the tighter design.

### F3 · Terminal sandbox disabled — 🟠 MEDIUM

- **What:** `enableTerminalSandbox` is not set (defaults to `false`) — shell commands execute unsandboxed.
- **Evidence:** `[48]` §1 and §10.
- **Live check:** still unset.
- **Recommendation:** `"enableTerminalSandbox": true` if you run untrusted repos/scripts. Sandboxing uses `sandbox-exec` on macOS; it pairs well with F1 reverting to `request-review`.

### F4 · `trustedWorkspaces` ≈ whole home directory — 🟠 MEDIUM

- **What:** 68 paths at audit time, **95 now**, including `~`, `~/Downloads`, `~/developer`, `~/Developer`, `~/.gemini`, `~/.gemini/config`, `~/obsidian`, `~/MyMacBookStuffs`.
- **Evidence:** `[1]` settings lines 70–138 (the list was truncated in the tool output — the agent counted 68); `[48]` §1 reports the count.
- **Why it matters:** `trustedWorkspaces` is a *whitelist*; when it includes your home directory, it stops meaning anything.
- **Live check:** 95 entries.
- **Recommendation:** Prune to the repos you actually trust (this repo, `google-antigravity-docs`, your plugin/skill projects). The stale-path problem only grows.

### F5 · Broad `unsandboxed(...)` allowlist — 🟠 MEDIUM

- **What:** 35 allow rules at audit time, **44 now** — `unsandboxed(agy)`, `unsandboxed(find|cat|ls|file|defaults|echo|head|tail|mkdir|mv|cp|ln|grep|wc)`, `unsandboxed(git add|status|log|diff)`, `unsandboxed(pip install llms-txt)`, `command(fd|rg|tokei|scc|ast-grep)`, etc.
- **Evidence:** `[1]` settings lines 7–52.
- **Why it matters:** `unsandboxed(...)` is fine for read-only utilities, but `pip install`, `python3 -c`, and `git add/commit` run without sandbox or review.
- **Live check:** 44 rules.
- **Recommendation:** Keep read-only tools; drop `unsandboxed(pip install ...)`, the ad-hoc `python3 -c` one-liners, and `git` write commands to `command(...)` (reviewed) instead.

### F6 · Denylist is thin — 🟡 LOW

- **What:** Only `read_file(.../.opencode)`, `command(rm -rf /)`, `command(wget)` are denied.
- **Evidence:** `[1]` settings lines 54–58.
- **Live check:** unchanged.
- **Recommendation:** Consider `command(osascript)`, `command(curl)` (or at least `curl | sh`), and `command(sudo)` if you don't need them — cheap insurance.

### F7 · `keybindings.json` missing — ⚪ INFO

- **What:** The file does not exist; default keybindings are in effect. The agent's first read attempt failed with an invalid-tool-call error and retry guidance (`Retries remaining: 4`) — a nice real-world example of the ERROR_MESSAGE schema.
- **Evidence:** `[11]` (ERROR_MESSAGE: *"failed to read file ... keybindings.json: no such file or directory"*); `[48]` §9.
- **Live check:** still absent.
- **Recommendation:** Nothing to fix — defaults are fine. Create the file only if you want custom shortcuts.

### F8 · Configured vs session model mismatch — ⚪ INFO

- **What:** `settings.json` pins `"model": "Gemini 3.5 Flash (Low)"` (settings line 5), but this session opened with *"changed setting Model Selection from None to Gemini 3.6 Flash (High)"*.
- **Evidence:** `[0]` (USER_SETTINGS_CHANGE metadata); `[1]` settings line 5.
- **Live check:** config still says `Gemini 3.5 Flash (Low)`.
- **Why it matters:** Session selection overrides the config default — not a bug, but if you always pick the same model interactively, update `settings.json` so headless `-p` runs use the model you actually want.

### F9 · Hooks ecosystem is active — ⚪ INFO

- **What:** `self-customizer/hooks.json` (PreToolUse JSON-validity checks, PostToolUse `agy --version` health checks), `i-have-adhd/hooks.json` (SessionStart `always-on.sh`), a 37 KB statusline quota script, and **two** trusted-hooks files (`~/.gemini/config/trusted_hooks.json` 2 B, `~/.gemini/trusted_hooks.json` 646 B).
- **Evidence:** `[15]` (FIND: 9 hooks files); `[48]` §7.
- **Live check:** all present.
- **Recommendation:** Keep hook timeouts tight (currently 5 s); the 2-byte `config/trusted_hooks.json` looks like a leftover — verify it's intentional.

### F10 · Plugin/MCP footprint — ⚪ INFO

- **What:** 15 plugins (8 claude-code, 6 antigravity, 1 gemini-cli); 7 of them carry `mcpServers` components; `mcp_config.json` defines `pieces` (`/opt/homebrew/bin/pieces mcp start`) and `sequential-thinking` (`npx -y @modelcontextprotocol/server-sequential-thinking`).
- **Evidence:** `[2]` (`agy plugin list` output); `[9]` (mcp_config.json); `[48]` §2, §6.
- **Live check:** identical.
- **Recommendation:** The `npx -y` server pulls code from npm on first run — fine for trusted packages; keep an eye on the 8 claude-code imports (they also ship 7 MCP server definitions you may not use).

---

## 4. Live Cross-Check (2026-08-11, ~11:00 +06:00)

| Surface | Audit snapshot (02:52) | Live now | Match |
|---|---|---|---|
| `allowNonWorkspaceAccess` | `true` | `true` | ✅ |
| `toolPermission` | `always-proceed` | `always-proceed` | ✅ |
| `enableTerminalSandbox` | unset | unset | ✅ |
| `editor` / `altScreenMode` / `notifications` | `code` / `always` / `true` | same | ✅ |
| `permissions.allow` | 35 rules | **44 rules** | ⚠️ grew |
| `permissions.deny` | 3 rules | 3 rules | ✅ |
| `trustedWorkspaces` | 68 paths | **95 paths** | ⚠️ grew |
| `ui.footer.items` | 9 items | 9 items | ✅ |
| `keybindings.json` | missing | missing | ✅ |
| Plugins | 15 | 15 | ✅ |
| MCP servers | `pieces`, `sequential-thinking` | same | ✅ |
| Hooks / trusted_hooks | present | present | ✅ |
| Agents | 3 (`code-reviewer`, `documentation-writer`, `self-auditor`) | 3 | ✅ |
| Global skills | 62 symlinks + 28 packages | 61 + 83 items (count method differs) | ⚠️ approximate |
| Rules (`GEMINI.md`, `global.md`) | present | present | ✅ |

All 10 findings verified; **no finding was refuted by the live config.**

---

## 5. Prioritized Recommendations

1. **Do now (5 min):** revert `toolPermission` to `request-review` and set `allowNonWorkspaceAccess` to `false`.
2. **Do next:** prune `trustedWorkspaces` from 95 to the repos you actually trust.
3. **Do when you have a spare hour:** trim the `unsandboxed(...)` allowlist to read-only utilities; consider `enableTerminalSandbox: true`.
4. **Optional hardening:** extend the denylist (`osascript`, `curl | sh`, `sudo`); check the 2-byte `trusted_hooks.json`; align `settings.json` `model` with your usual session pick.

None of these were applied — this report is advisory only.

---

## 6. Regenerating This Report

The audit itself is one command in the CLI — run the `self-auditor` agent (`agy agents`, then pick it, or `agy --agent self-auditor -p "audit my configuration"` in headless mode).

To re-verify findings against the live config after changes, re-run the read-only probes in §4 (a future task could turn this into `scripts/audit_config.py`). Regenerate this report whenever `settings.json` or the plugin set changes.

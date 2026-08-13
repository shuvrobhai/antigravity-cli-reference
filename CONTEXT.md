# antigravity-cli-reference Context

A knowledge-assistant skill that answers questions about the Google Antigravity CLI from verified, source-tagged data instead of guessing — and learns from its own runtime through a session journal.

> For operational guidelines, build/lint/test command references, and repository architecture, see [AGENTS.md](file:///Users/rayhanislamshuvro/Developer/ClearContextProject/antigravity-cli-reference/AGENTS.md).

## Language

**Antigravity CLI (agy)**:
The Google command-line interface for directing coding agents. The sole subject of this skill's knowledge.
_Avoid_: Gemini CLI, the product

**Knowledge file**:
The machine-readable, source-and-confidence-tagged canonical reference for the Antigravity CLI. The skill's first consult on every invocation.
_Avoid_: the JSON, the database

**Research document**:
The source-classified prose analysis from which the knowledge file is populated. Consulted only when the knowledge file is insufficient.
_Avoid_: the markdown, the doc

**Claim**:
A single fact in the knowledge file carrying `source` (DOCS/GOOGLE/PROTOCOL/COMMUNITY) and `confidence` (A/B/C) tags.
_Avoid_: fact, entry

**Session journal**:
The skill's running record of invocations — one-line summaries, plans, outcomes, reviews, and troubles — which accumulates real use cases over time.
_Avoid_: memory log, log

**Use case**:
A recurring purpose for invoking the skill. Every journal entry is keyed to a stable use-case slug so recurrence is countable.
_Avoid_: task, topic

**Targeted read**:
Consulting only the relevant slice of the knowledge file — grep the section key, then read that section — rather than the whole file.
_Avoid_: full read, load

**Tail read**:
Reading the most recent session-journal entries at the start of an invocation so prior sessions shape the current plan.
_Avoid_: history, state

**Permission gate**:
The user's approval checkpoint before the skill takes any side-effecting action.
_Avoid_: confirmation, approval (when the gate is meant)

**Trouble**:
A logged failure or knowledge gap encountered during an invocation, recorded for the self-improvement loop.
_Avoid_: bug, issue

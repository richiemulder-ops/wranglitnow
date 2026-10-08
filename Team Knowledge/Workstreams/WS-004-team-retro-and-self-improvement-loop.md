# WS-004 - Team Retro and Self-Improvement Loop

- **Status:** Active (since v4.0.0)
- **Type:** Workstream - a multi-agent composition. The team learns from its own run history and proposes improvements to itself. **Pre-canonicalized exception**, alongside [[WS-001-daily-journaling]], [[WS-002-import-external-knowledge-base]], and [[WS-003-install-an-expansion]] - it ships wired out of the box because the self-improvement loop must be governed from day one, never bolted on later.
- **Owners:** **Larry** (orchestrator - runs the Tier 2 retro, folds the Tier 1 check into close-session, routes every approved proposal to its implementer). **Every specialist** (Tier 0 and Tier 1 - each captures its own learnings and emits its own proposals). The **named implementer** per approved proposal (writes the actual change). **Silas** (mypka.db regen after any landed change). **The user** (the gate - approves the WHAT on every Tier 1 and Tier 2 change).
- **References:** [[GL-005-llm-agnostic-portable-core]] (proposals must keep the portable core clean), [[GL-001-file-naming-conventions]], [[GL-002-frontmatter-conventions]], [[SOP-create-task]], [[SOP-close-task]], [[SOP-write-journal-entry]], [[SOP-read-own-journal]], [[SOP-001-how-to-add-a-new-specialist]], [[SOP-002-convert-mypka-to-sqlite]], [[Team/agent-index]].
- **Triggered by:** natural-language phrasing that signals "the team should learn from itself" or "run the retro." See **Trigger contract** below. The close-session routine also runs the Tier 1 check every session and MAY nudge the Tier 2 retro on a roughly monthly cadence as an option (never automatically).

## Purpose

Let the team get better at its own work over time by mining what it has already learned - durable insights in `Team/*/journal/` and the run record in `session-logs/` - and turning recurring patterns into concrete, ranked improvement proposals. The team improves itself **by proposing**, never by self-rewriting. Every change to a contract, SOP, Workstream, Guideline, or `AGENTS.md` passes through a human gate.

## The hard invariant (read this first)

**Any edit to a specialist contract, an SOP, a Workstream, a Guideline, or any `AGENTS.md` is human-gated.** The team PROPOSES autonomously; it NEVER self-rewrites the framework. There is no autonomous path from "a specialist noticed something" to "the framework changed." The user approves the WHAT of every framework change before a named implementer writes it.

This is a deliberate contrast with autonomous self-evolving agents that rewrite their own instructions, skills, or prompts without a human in the loop. Wranglit is a **governed product**, not a self-modifying organism. The safety posture - the team can learn and propose, but a human always ratifies framework changes - is itself a v4 selling point: the buyer gets a team that compounds its competence without ever silently changing the rules out from under them.

The only autonomous tier is Tier 0, and Tier 0 by construction cannot touch the framework - it writes only to a specialist's own journal, which is non-binding reflective memory, not a contract.

## The three tiers

| Tier | What | When | Autonomy | Gate | Writes to |
|---|---|---|---|---|---|
| Tier 0 | Capture a durable learning | In-session, as it happens | Autonomous | None (reversible, non-binding) | `Team/<Name>/journal/` (own only) |
| Tier 1 | Emit a reusable learning as a proposal | In-session | Proposes autonomously | Human approves the WHAT | In-conversation + `Team Knowledge/tasks/open/` |
| Tier 2 | Team Retro - batch-mine patterns into a ranked proposal doc | On-demand (periodic nudge optional) | Proposes autonomously | Human approves a subset | `Deliverables/` |

## Trigger contract

| User says (or implies) | Action |
|---|---|
| (a specialist learns something durable mid-task) | **Tier 0** - the specialist writes a journal entry to its own `Team/<Name>/journal/` per [[SOP-write-journal-entry]] |
| (a specialist notices a learning that would help the WHOLE team, or a recurring friction) | **Tier 1** - emit a proposal in-conversation and write it as a task to `Team Knowledge/tasks/open/` |
| "run the team retro" / "let's do a retro" / "what has the team learned" / "where can the team improve" / "mine the journals" | **Tier 2** - run the full retro from §Tier 2 |
| (close-session routine, every session) | Run the **Tier 1 graduate-to-SOP check** (see §Tier 1) |
| (close-session routine, ~monthly, optional) | Larry MAY nudge: "It has been a while since the last team retro - want me to run one?" On-demand remains the default trigger; the nudge is only an offer |

---

## Tier 0 - In-session capture (autonomous, safe)

The cheapest tier. A specialist, mid-task, learns something durable - a working path past an error, a recipe that worked, a boundary it had to hold, a tool quirk - and captures it to its OWN journal.

1. The specialist writes a journal entry under `Team/<Name>/journal/` per [[SOP-write-journal-entry]] (the `## What I learned` / `## When this applies` / `## When this does NOT apply` shape).
2. That entry becomes a prior it (and only it) re-reads before future referenced work, per [[SOP-read-own-journal]].

Tier 0 is **autonomous, non-binding, and reversible**. It needs no gate because a journal entry changes no contract and binds no other specialist. It is reflective memory, nothing more. A specialist never writes to another specialist's journal and never edits the framework at this tier.

---

## Tier 1 - In-session proposal (human-gated)

When a learning is **reusable across the team** - it would improve a shared SOP, Guideline, Workstream, contract, or routing rule - it is no longer a private journal note. It becomes a PROPOSAL. It is never a direct framework edit.

### Step 1 - The specialist emits the proposal

The specialist (or Larry, noticing the pattern) states the proposal in-conversation: what was learned, what shared artifact it should change, and the specific proposed change.

### Step 2 - Write the proposal as a task

The specialist writes the proposal as a task to `Team Knowledge/tasks/open/` per [[SOP-create-task]], populating the `linked_*` arrays (the SOP/WS/GL it would touch, the journal entry that prompted it, the session log). The task is the durable, reviewable record of the proposal. **The task is the proposal - it is not the change.**

### Step 3 - Larry routes; the user approves the WHAT

Larry surfaces the proposal to the user and routes it to the right implementer (e.g. a Guideline change goes to its owner; a new specialist goes to Nolan per [[SOP-001-how-to-add-a-new-specialist]]). **The user approves the WHAT** before anything is written.

### Step 4 - The named implementer writes it

Only after approval does the named implementer make the change, claiming and closing the task per [[SOP-close-task]]. Any change that touches the portable core must keep it clean per [[GL-005-llm-agnostic-portable-core]].

### The close-session graduate-to-SOP check

Fold this check into the close-session routine, every session:

> **Did anything this session cross the graduate-to-SOP threshold?** That is: did a one-off approach prove itself reusable enough that it should become (or amend) a shared SOP, Guideline, or Workstream rather than staying a private journal note?

If yes, raise it as a Tier 1 proposal here (Steps 1 to 2) before the session closes. If no, the routine moves on. This is the standing mechanism that keeps durable learnings from dying in individual journals.

---

## Tier 2 - The Team Retro (periodic batch, human-gated)

The Team Retro is the heavy, batch pass. It runs **on-demand** ("run the team retro") by the user's decision. Close-session MAY nudge it roughly monthly as an option, but on-demand is the default trigger - the retro never fires on its own.

### Step 1 - Larry: mine the inputs

Larry reads the full run history:

- Every `Team/*/journal/` entry across all specialists.
- The `session-logs/` record.
- The open and recently-closed tasks (for Tier 1 proposals already raised but not yet acted on).

### Step 2 - Larry: cluster the patterns

Larry clusters what it finds into recurring patterns. At minimum:

- **Repeated anti-patterns** - the same friction, mistake, or dead-end showing up across multiple sessions or specialists. Candidates for a new guardrail in a contract or Guideline.
- **Recipes that cleared the bar** - approaches that worked repeatedly and deserve to graduate into a shared SOP, Guideline, or Workstream.
- **Dead or unfollowed SOPs** - procedures that the run record shows nobody actually uses, or that get routinely worked around. Candidates for archive or rewrite.

### Step 3 - Larry: emit a RANKED proposal document

Larry writes a single ranked proposal document to `Deliverables/` (`Deliverables/YYYY-MM-DD-team-retro-proposals.md`). Each proposal carries: the pattern and its evidence (which journals / session-logs / how many times), the proposed change, the artifact it touches, the named implementer, and a rank. The document **proposes**; it changes nothing.

### Step 4 - The user approves a subset

The user reviews the ranked list and approves a subset. Nothing is approved by default. Unapproved proposals stay in the document as a backlog for the next retro.

### Step 5 - Implementers land the approved subset

Each approved proposal goes to its named implementer, who makes the change (claiming/closing a task per [[SOP-close-task]] where one was raised). Portable-core changes keep the core clean per [[GL-005-llm-agnostic-portable-core]]. Archiving a dead SOP follows the no-renumber rule in [[GL-001-file-naming-conventions]] - the gap is acceptable.

### Step 6 - Silas: mypka.db regen

After the approved subset has landed, Silas regenerates the SQLite mirror per [[SOP-002-convert-mypka-to-sqlite]] so the derived index reflects the new framework state. Markdown is canonical; the DB is downstream.

### Step 7 - Larry: session-log the retro

Larry writes a session-log entry capturing: when the retro ran, how many patterns were clustered, which proposals were approved vs deferred, who implemented what, and the regen result.

---

## Edge cases

| Situation | Behaviour |
|---|---|
| A specialist wants to change a shared artifact directly mid-task | Not allowed. It becomes a Tier 1 proposal. The hard invariant holds. |
| A Tier 2 proposal would couple the portable core to a harness | Implementer routes the mechanism into the adapter layer per [[GL-005-llm-agnostic-portable-core]]; the portable change stays clean. |
| The retro surfaces a gap no current specialist covers | The proposal is "hire a specialist" - routed to Nolan per [[SOP-001-how-to-add-a-new-specialist]] after the user approves. |
| User approves nothing in the retro doc | Fine. The document stays as backlog; nothing changes. The retro never forces a change. |
| Same proposal recurs across multiple retros, never approved | It stays in the backlog. Recurrence is signal for the user, not grounds for autonomous action. |

---

## Owner agency

Each tier's owner owns their part. Specialists own Tier 0 capture and Tier 1 proposal emission for their own domain. Larry owns the orchestration shell - the Tier 1 close-session check, the Tier 2 retro run, and routing every approved proposal to its implementer. The named implementer owns the actual write. Silas owns the regen. **The user owns the gate, always.** No owner may collapse a tier's gate.

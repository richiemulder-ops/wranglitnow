# WS-001 - Daily Journaling

- **Type:** Workstream — a multi-agent composition. The agents below collaborate to deliver the outcome. New Workstreams emerge when patterns repeat across session-logs; this one ships pre-canonicalized because daily journaling is a day-1 flow.
- **Owners:** Penn (capture and writing), Larry (routing and Librarian pass)
- **References:** [[SOP-001-how-to-add-a-new-specialist]], [[GL-001-file-naming-conventions]], [[Team/Penn - Journal Writer/AGENTS]], [[Team/Larry - Orchestrator/AGENTS]]
- **Trigger:** any user input that contains a thought, observation, encounter, screenshot, photo, or voice note.
- **Version:** 1.1.0 (2026-06-03) — Step 4 routing now enforces the My Life doctrine: every Goal anchors to exactly one Key Element, names a single carrier (Project OR Habit), passes the filter test, and Topics graduate into Key Elements rather than deepening forever. See the dated note at the foot of this file.

## Purpose

Turn raw daily inputs into structured PKM entries. The Journal is the inbox. People, organizations, and topics referenced in journal entries get cross-linked into the CRM and My Life sections.

## Inputs

- **Text** - the user types or pastes a thought.
- **Image** - the user drops a screenshot, photo, or business card.
- **Audio** - the user shares a voice note (transcribed by the LLM if it can; otherwise stored and flagged).

## Choreography

### Step 1 - Larry receives the input

Larry checks the routing cheatsheet in his AGENTS.md. Daily journaling triggers route to Penn.

### Step 2 - Penn writes the Journal entry

- **Path:** `PKM/Journal/YYYY/MM/YYYY-MM-DD-<slug>.md`.
- **Auto-create folders:** if `YYYY/` or `YYYY/MM/` does not exist, Penn creates them.
- **Filename:** ISO date prefix plus a kebab-case slug derived from the day's main theme. See [[GL-001-file-naming-conventions]].
- **Format:** plain markdown. One entry per day. If the day already has an entry, Penn appends a new section to the existing file.

### Step 3 - Penn handles images

- **Path:** `PKM/Images/YYYY/MM/YYYY-MM-DD-<slug>.<ext>`.
- **Auto-create folders:** same rule as Journal.
- **Filename pattern:** see [[GL-001-file-naming-conventions]].
- **Embed in Journal:** Penn embeds the image in the Journal entry with `![[Images/YYYY/MM/YYYY-MM-DD-<slug>.<ext>]]`. The image lives in `PKM/Images/`. The Journal entry references it. Image is never duplicated into the Journal folder.

### Step 4 - Penn cross-links to PKM

For each entity mentioned in the input, Penn routes by type. Use the table below as the routing map:

| Type of mention | Destination folder | Filename pattern | Notes |
|---|---|---|---|
| Person | `PKM/CRM/People/` | `firstname-lastname.md` (or `title-lastname.md`) | Stub if missing. Embed any business card or photo via `![[Images/...]]`. |
| Organization, company, venue | `PKM/CRM/Organizations/` | `<org-slug>.md` | Stub if missing. Cross-link to People who work there. |
| Interest area or recurring subject | `PKM/My Life/Topics/` | `<topic-slug>.md` | Stub if missing. Topics are the signal layer, not projects. If the interest has crystallized into a measurable pursuit, propose promoting it to a Key Element — don't just deepen the Topic. |
| Habit, ongoing rhythm, routine | `PKM/My Life/Habits/` | `<habit-slug>.md` | Stub if missing. Habits have a cadence, no finish line. A Habit is one of the two carrier shapes for a Goal (the sibling of a Project). |
| Concrete time-bound effort | `PKM/My Life/Projects/` | `<project-slug>.md` | Stub if missing. Projects have a finish line. A Project is one of the two carrier shapes for a Goal (the sibling of a Habit). |
| Outcome or aspiration with horizon | `PKM/My Life/Goals/` | `<goal-slug>.md` | Stub if missing. Goals are the operating layer, not a bucket. Anchor each Goal to exactly one Key Element (never a Project, never a Topic) and name its single carrier — a Project OR a Habit, never both. |
| Stable life dimension (Health, Family, Career, etc.) | `PKM/My Life/Key Elements/` | `<element-slug>.md` | Stub if missing. Key Elements are the load-bearing walls — every Goal anchors to one of these. Topics graduate into here once they crystallize. |
| Real-world document (passport, contract, certificate, ID) | `PKM/Documents/` | `<doc-slug>.md` | Stub if missing. Document records hold metadata: physical location, digital location, expiry, renewal trigger. The actual file (if scanned) goes under `PKM/Images/` and is embedded. |

For every routed entity:

- If a file already exists at the destination, Penn `[[wikilinks]]` to it from the Journal entry. No restating biographical or contextual details that already live in the canonical file.
- If no file exists, Penn creates a stub at the right path with the minimum content needed for the link to resolve, then `[[wikilinks]]` to it from the Journal entry.

This is how the Journal becomes the connective tissue of your Wranglit.

### Step 4a - Decision rule: stub vs inline mention

Create a stub when the entity has any of:

- A name the user is likely to refer to again (people, organizations, recurring topics).
- A property the user will want to retrieve later (passport expiry, project finish line, goal horizon).
- Cross-cutting relevance (a person who appears in multiple contexts, a topic that recurs).

Inline-mention only (no stub) when:

- The reference is a one-off and clearly will not return (a passing name, a one-time anecdote).
- The user explicitly says "don't file this" or similar.

When in doubt, create the stub. A stub costs nothing. A missing reference costs the wiki its connectivity.

### Step 4b - My Life doctrine enforcement

Before stubbing or linking anything in `PKM/My Life/`, run the doctrine checks. My Life is four buckets (Topics, Habits, Projects, Key Elements) plus Goals as the operating layer on top — not five flat buckets.

1. **The filter test.** Does this belong in My Life at all? My Life holds the concepts you actively work with — walls, rhythms, pushes, signals. Reference facts, contacts, and documents live elsewhere (CRM, Documents). If the candidate is not a Topic, Habit, Project, Key Element, or Goal, route it out of My Life.
2. **The anchoring law.** Every Goal anchors to **exactly one Key Element — never a Project, never a Topic.** When stubbing a Goal, name its Key Element. If the Goal points at something that is not yet a Key Element, that something is either a Topic awaiting promotion or a misframed Goal — do not anchor a Goal to a Topic. Example: the Goal *"lose 20 kg"* anchors to the Key Element [[health]].
3. **The single-carrier rule.** A Goal is carried by **one carrier — a Project OR a Habit, never both, never neither.** Projects and Habits are siblings: a Project when the work has a finish line, a Habit when it is an open-ended rhythm. Example: *"lose 20 kg"* is carried **either** by a Project (an 8-week program) **or** by a Habit (3 workouts a week) — pick one. If both seem needed, split the Goal or pick the dominant carrier.
4. **Topic to Key Element promotion.** A Topic is where a new interest lands first. When a Topic crystallizes into a measurable pursuit the user intends to drive, propose **promoting it into a Key Element** — only then can a Goal anchor to it. Don't keep deepening a Topic that has become a pursuit. Example: *French* starts as a Topic; when it sharpens into "reach B2 fluency," it graduates into a Key Element, and a Goal can anchor there. The reverse holds too: a Key Element with no anchored Goals and no active push gets archived back down.

These checks are proposals at capture time. Penn stubs the doctrine-correct shape and flags any anchor/carrier ambiguity to Larry rather than guessing.

### Step 5 - Larry's Librarian pass at session close

At session close, Larry scans the new Journal entry, the new image (if any), and any newly created CRM or My Life stubs:

- Confirms `[[wikilinks]]` resolve.
- Confirms images sit in `PKM/Images/YYYY/MM/`, not duplicated elsewhere.
- Confirms each new stub is listed in its section's `INDEX.md`.
- Flags SSOT violations to the user.

## What this Workstream does not do

- Does not write business workflows. Those are handled by future specialists hired through Nolan via [[SOP-001-how-to-add-a-new-specialist]].
- Does not produce research reports. Pax handles that.
- Does not edit the user's existing CRM entries. Penn appends, never overwrites, unless the user asks.

## Naming and image rules

All naming questions resolve to [[GL-001-file-naming-conventions]]. If you need to know how to name a slug, what date format to use, or how to handle filename collisions, look there. Do not restate naming rules inside this Workstream.

## Changelog

- **1.1.0 (2026-06-03)** — Step 4 routing rewritten to enforce the My Life doctrine. My Life is now framed as four buckets (Topics, Habits, Projects, Key Elements) plus Goals as the operating layer on top. Added Step 4b: the filter test, the anchoring law (every Goal → exactly one Key Element, never a Project/Topic), the single-carrier rule (Project OR Habit, siblings, never both), and Topic→Key-Element promotion with reverse archive. Routing-table notes for the five My Life types updated to match. Canonical examples woven in: the weight Goal ("lose 20 kg" → Key Element Health, carried by an 8-week Project or a 3-workouts-a-week Habit) and the French Topic (graduates into a Key Element once it becomes "reach B2 fluency").
- **1.0.0** — Initial day-1 daily-journaling flow.

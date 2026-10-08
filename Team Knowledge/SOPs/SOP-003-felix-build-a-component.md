# SOP: Build a Component

> **Default owner:** Felix. Any agent can invoke this skill.

Felix's signature workflow for building a UI component end-to-end with design-system fidelity, type safety, accessibility, and a clean handoff to Vera's quality gate.

## When this skill activates

Trigger phrases — invoke this SOP when the user (via Larry) says any of:

- "build me a [component / button / form / card / modal / widget / panel]"
- "I need a [thing] in the UI"
- "scaffold a new component for [purpose]"
- "create a reusable [primitive]"
- "extract this into a component"
- "refactor this inline JSX into a proper component"

If the request is "fix this component" or "this UI is broken," that's frontend triage, not a clean build — Felix can still use this SOP as a reference, but the inspect/refactor workflow is lighter than the new-build workflow below.

## Procedure

### 1. Read the spec, then the codebase

Before writing a single line of code:

1. **Confirm the spec.** What does the component do, what are its inputs, what are its states (loading / empty / error / success / disabled)? If any of these are ambiguous, ask the user before proceeding. Building the wrong thing fast is slower than asking once.
2. **Read your team's design system** at `Team Knowledge/Guidelines/GL-003-design-system.md` if it exists. Note the relevant tokens (color, typography, spacing, radius, animation), primitive components already in your stack, and any banned patterns.
3. **Inspect the existing codebase.** Glob for similar components. Read the closest existing match. Match the project's conventions — file structure, naming, import style, prop interface style. Don't introduce a new pattern; match the prevailing one.

### 2. Decide where it lives

Component placement matters. The team's component architecture probably falls into one of three patterns:

- **Global** (e.g., `src/components/` or equivalent): used across the whole app or multiple apps.
- **Shared** (e.g., `src/apps/_shared/`): used by two or more apps but not globally.
- **App-specific** (e.g., `src/apps/<app>/components/`): used by exactly one app, never imported elsewhere.

Pick the narrowest scope that fits today's need. You can always promote later. Promoting prematurely is harder than promoting on demand.

### 3. Scaffold with semantic tokens

Write the component using **only** semantic design-system tokens. No hardcoded colors. No hardcoded font sizes. No magic spacing values. If a token doesn't exist for what you need, stop, propose the new token to the user (or to Iris if she's on the team), and wait for approval before inventing one.

Skeleton (adapt to your stack):

```tsx
// One illustrative line of intent — adapt to your stack
<div className="bg-surface text-body p-md rounded-md">...</div>
```

Banned (in any stack):

- Hardcoded colors: `bg-[#000]`, `color: #ff5500`, `bg-zinc-900/15`
- Hardcoded sizes: `text-[14px]`, `font-size: 13px`
- Browser dialogs in place of designed surfaces: `window.confirm`, `alert`
- Truncation classes when your design system has a sanctioned fade/ellipsis primitive

### 4. Type every prop and every API contract

If the project is typed (TypeScript, Flow, etc.), type the component completely. Every prop. Every callback. Every piece of data the component renders. No `any`. No implicit any. No `@ts-ignore` without an inline comment explaining exactly why.

If the component fetches or mutates data, the request shape and the response shape get types too. Don't let an untyped network boundary into the component.

### 5. Handle every state explicitly

Every component renders at least one of these states; most render several. Walk through each and make sure the component handles it visibly:

- **Loading** — what does the component look like while data is in flight? Skeleton, spinner, deferred render?
- **Empty** — what does it look like when there's nothing to show? Empty-state messaging?
- **Error** — what does it look like when something failed? Recoverable? Retry affordance?
- **Success** — the happy path.
- **Disabled / read-only** — if applicable.
- **Interactive states** — hover, focus, active, focus-visible.

Skipping any of these is a deferred bug.

### 6. Accessibility from the first commit

Bake it in. Don't retrofit:

- **Semantic HTML.** Use the right element. Buttons are `<button>`. Links are `<a>`. Headings are `<h1>`–`<h6>` in document order.
- **Keyboard navigation.** Every interactive element must be reachable and operable with a keyboard. Tab order makes sense. Escape closes overlays. Enter and Space activate buttons.
- **Focus indicators.** Visible. Always. Never `outline: none` without a replacement.
- **ARIA when HTML isn't enough.** `aria-label`, `aria-labelledby`, `aria-describedby`, `role` — used sparingly and correctly. Don't sprinkle ARIA; use it when semantics are missing.
- **Color contrast.** Body text and interactive text against their background must clear WCAG 2.2 AA (4.5:1 for normal text, 3:1 for large text and UI components). If your design tokens are well-chosen this is automatic; if they aren't, flag it.

### 7. Performance as a reflex

Don't over-optimize, but don't under-think:

- **Lazy-load heavy children.** Modals, charts, rich editors, anything large.
- **Memoize obvious recomputations.** Don't spray `useMemo` everywhere; use it where the cost is real.
- **Don't bypass the project's state layer.** If your stack has a Zustand store / React Query / Redux / equivalent, mutate through it. Don't reach into the database from the component.
- **Measure before optimizing.** If you suspect a perf issue, profile. Don't guess.

### 8. Verify visually before declaring done

TypeScript compiling is necessary but not sufficient. Before handing off to Vera:

1. **Render it.** Run the dev server. Look at the component in the browser.
2. **Check three breakpoints.** Mobile (375px), tablet (768px), desktop (1280px).
3. **Check both color modes** if the project has light and dark.
4. **Tab through it.** Confirm focus order, focus indicators, keyboard activation.
5. **Trigger every state.** Loading, empty, error, success, disabled, hover, focus.

If anything looks wrong, fix it now. Vera's gate is faster when you've already cleared the obvious self-checks.

### 9. Write the session-log entry

At `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_felix_<component-slug>.md`. Capture what you built, which design tokens you used or extended, any pattern decisions worth preserving, and any follow-ups (e.g., "needs a Storybook story," "tablet breakpoint feels tight, may need a redesign pass").

### 10. Hand off to Vera

The build isn't done until Vera signs off. Larry routes the deliverable to Vera; Vera runs [[SOP-005-vera-quality-gate]] and returns a pass/fail. If Vera flags issues, fix them, then resubmit. Don't argue the gate.

## Output / definition of done

A component build is done when **all** of these are true:

- [ ] Component lives in the correct architectural layer (global / shared / app-specific).
- [ ] Uses only semantic design-system tokens. No hardcoded colors, sizes, or spacing.
- [ ] Fully typed (every prop, every API contract).
- [ ] Handles loading, empty, error, success, disabled, and interactive states.
- [ ] Keyboard-navigable, with visible focus indicators.
- [ ] Color contrast clears WCAG 2.2 AA.
- [ ] Renders correctly at mobile, tablet, and desktop breakpoints.
- [ ] Renders correctly in both color modes (if applicable).
- [ ] Session-log entry written.
- [ ] Vera's quality gate signed off.

If any box is unchecked, the component isn't shipped. It's "in progress."

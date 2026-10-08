# SOP: Quality Gate

> **Default owner:** Vera. Any agent can invoke this skill.

Vera's signature workflow for the visual + accessibility + responsive QA pass. Every UI deliverable clears this gate before it ships. Produces a structured, severity-tagged report with screenshot evidence and a clear pass/fail verdict.

## When this skill activates

Trigger phrases — invoke this SOP when the user (via Larry) says any of:

- (Felix or another agent finishes UI work and Larry calls Vera before marking the task complete)
- "QA this [page / component / flow / dashboard]"
- "is this ready to ship?"
- "audit accessibility"
- "responsive check"
- "design-system drift check"
- "this UI feels off but I can't say why"

Any UI work — new build, refactor, bug fix, redesign — passes through this gate. No skips.

## Procedure

The gate runs in six phases. Don't skip phases — accessibility issues hide behind visual issues hide behind responsive issues.

### Phase 1 — Preparation

1. **Read the design system.** If your team has one at `Team Knowledge/Guidelines/GL-003-design-system.md`, read it now, every time. It may have changed since the last gate. Note the relevant tokens, components, and rules you'll be checking against. If GL-003 doesn't exist, the first finding is its absence — recommend the team document the design system as a prerequisite for any future quality gate that hopes to be objective.
2. **Read the spec.** What was the deliverable supposed to do? What did Felix (or whoever built it) hand off? If the spec is unclear, ask before inspecting.
3. **Open the deliverable.** Browser, dev server, deployed preview — wherever it lives.

### Phase 2 — Screenshot capture

Visual evidence is the foundation of every finding. Without it, the gate is just opinion.

1. **Capture the deliverable in its primary state.** Full-page screenshot at desktop width (1280px or your team's primary breakpoint).
2. **Capture each major state.** Loading, empty, error, success, disabled, hover, focus — whichever apply.
3. **Capture each breakpoint.** Mobile (375px), tablet (768px), desktop (1280px) at minimum. If your team supports more, include them.
4. **Capture both color modes** if the project has light and dark.
5. **Save screenshots** alongside the QA report, in a sibling folder if more than two or three accumulate.

If browser-automation tooling isn't available in your runtime, ask the user to provide screenshots. Don't run the gate from imagination — visual inspection requires visual evidence.

### Phase 3 — Visual analysis

For every screenshot, walk through these checks:

1. **Color tokens.** Every color visible — backgrounds, text, borders, accents — should resolve to a design-system token. Hardcoded values are findings. If your team's design system declares a banned-values list, those are CRITICAL findings (someone reintroduced a retired identity).
2. **Typography.** Font family, size, weight, line height — all from the design system's typography scale. Hardcoded `text-[14px]` or arbitrary `font-weight: 600` are findings.
3. **Spacing.** Padding, margin, gaps — from the spacing scale. Magic numbers (`padding: 13px`) are findings.
4. **Radius.** Corner radius from the design system. One-off `rounded-[7px]` is a finding.
5. **Component fidelity.** If the deliverable uses or extends a primitive that already exists in the design system, it should match the primitive's behavior. If it's a custom variant, that's a finding worth flagging — could it have been the existing primitive?
6. **State coverage.** Every interactive state (hover, focus, focus-visible, active, disabled) is visually distinct. Missing focus-visible is a HIGH finding; missing hover is a MEDIUM.
7. **Hierarchy.** Visual hierarchy reads correctly. Primary action is most prominent. Secondary actions are subordinate. Destructive actions are clearly marked. Headings are larger than body text and increase in importance toward the top of the page.
8. **Alignment and rhythm.** Things that should align, align. Vertical rhythm is consistent. Cramped or sparse zones are flagged.
9. **Imagery and iconography.** Icons consistent across the design system (one icon set, not three). Images load with proper aspect ratios (no shifting, no broken `alt`).
10. **Empty / error / loading states.** All present, all on-brand, all useful (no "Error" with no recovery affordance).

### Phase 4 — Responsive verification

For every breakpoint screenshot, walk through:

1. **No horizontal scroll** unless intentional (a wide table, an explicit pan).
2. **Tap targets at mobile** are at least 44×44 CSS pixels (WCAG 2.5.5 / 2.5.8). Tiny mobile tap targets are HIGH findings.
3. **Text remains readable** at every breakpoint. Doesn't shrink below the design system's minimum body size. Doesn't overflow its container.
4. **Layout reflows sensibly.** Multi-column desktop layouts collapse to single-column on mobile in a logical reading order.
5. **No clipping or truncation** of important content at any breakpoint.
6. **Images and media reflow.** Aspect ratios preserved. No squashed or stretched media.

### Phase 5 — Accessibility audit (WCAG 2.2 AA)

Non-negotiable. Every gate, every time:

1. **Color contrast.** Body text 4.5:1 against its background. Large text (18pt or 14pt bold) and UI components 3:1. Test the actual rendered values, not the design system's claimed values — token drift can break contrast.
2. **Focus indicators.** Every focusable element has a visible focus ring when reached by keyboard. `outline: none` without a replacement is a HIGH finding.
3. **Keyboard navigation.** Tab through the entire deliverable. Confirm:
   - Tab order matches the visual order.
   - Every interactive element is reachable.
   - Every interactive element is operable (Enter / Space / arrow keys as appropriate).
   - Escape closes overlays.
   - Focus traps in modals (focus stays inside, returns to the trigger on close).
4. **Semantic HTML.** Buttons are `<button>`. Links are `<a>`. Headings are `<h1>`–`<h6>` in document order. A `<div>` with `onClick` and no role is a finding.
5. **ARIA correctness.** Where ARIA is used, it's used correctly. `aria-label` on icon-only buttons. `aria-labelledby` linking to existing IDs. `role="dialog"` on modal containers with `aria-modal="true"`. Misused or redundant ARIA is a finding.
6. **Form labels.** Every input has an associated `<label>`. Placeholder text is not a label.
7. **Motion respect.** If the deliverable uses animation, `prefers-reduced-motion` is honored. Aggressive animation that ignores the user preference is a HIGH finding.
8. **Image alternatives.** Decorative images have `alt=""`. Meaningful images have descriptive `alt`. SVGs that convey meaning have `<title>` or `aria-label`.

### Phase 6 — Report generation

Write the report at `Deliverables/YYYY-MM-DD-<slug>-qa-report.md`. Structure:

```
# QA Report: <deliverable name>

**Inspector:** Vera
**Date:** YYYY-MM-DD
**Verdict:** PASS | FAIL | CONDITIONAL PASS

## Summary

<2-3 sentences: what was inspected, top-level result, top-priority finding>

## Findings

### [SEVERITY] <Short title>

**Where:** <component / page / breakpoint>

**What:** <one-paragraph description with screenshot reference>

**Cited rule:** <design system rule, WCAG criterion, or responsive guideline>

**Fix recommendation:** <specific and actionable>

(repeat per finding)

## Verdict

<PASS / FAIL / CONDITIONAL PASS, with a one-sentence rationale>
```

## Severity ladder

- **CRITICAL** — accessibility blocker (a screen reader can't reach core functionality, contrast fails on primary text, keyboard navigation is broken) or design-system contract violation that can't ship (banned values reintroduced). Hard fail.
- **HIGH** — major drift from the design system, broken responsive behavior at a primary breakpoint, missing focus indicators on interactive elements. Hard fail.
- **MEDIUM** — minor drift, missing hover states, sub-optimal but functional accessibility, inconsistent spacing rhythm. Soft fail (CONDITIONAL PASS with required follow-up).
- **LOW** — polish suggestions, nice-to-haves, future-state recommendations. Backlog.

## Verdict rules

- **PASS** — no CRITICAL or HIGH findings. MEDIUM and LOW findings are documented but don't block.
- **CONDITIONAL PASS** — no CRITICAL findings, no more than two HIGH findings, all of which have an agreed fix path. The deliverable can ship if the user explicitly accepts the conditions.
- **FAIL** — any CRITICAL finding, or three or more HIGH findings. The deliverable does not ship until fixes are applied and Vera re-inspects.

Vera does not negotiate verdicts under pressure. The gate is the gate.

## Output / definition of done

A quality gate pass is done when **all** of these are true:

- [ ] All six phases completed (preparation, screenshot capture, visual, responsive, accessibility, report).
- [ ] Every finding has a screenshot reference, a cited rule, and a fix recommendation.
- [ ] Verdict is unambiguous: PASS, CONDITIONAL PASS, or FAIL.
- [ ] Report is at `Deliverables/YYYY-MM-DD-<slug>-qa-report.md`.
- [ ] Session-log entry written at `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_vera_<slug>.md` capturing methodology and recurring patterns worth flagging to the team.
- [ ] If FAIL, the responsible specialist (usually Felix) is notified via Larry with the report attached.
- [ ] If a fix happens, Vera re-inspects. No second-hand confirmation.

If the gate found CRITICAL issues that block shipping, the verdict line states that explicitly. Urgency does not get lost in the body of the report.

---
id: GL-003
title: Design System
owner: Iris
status: active
---

# GL-003 — Wranglit Design System

The visual single source of truth. Iris owns this file. Charta, Pixel, Felix and
Vera all read from it and none of them re-declare a token. If a value is not here,
it does not exist — add it here first, then use it.

This is a starting system, not a finished brand. It is deliberately neutral so you
can make it yours. See §9 for how to rebrand it in one pass.

---

## 1. Name and casing

The system is **Wranglit**. Capital W, everything else lowercase. Never WrangLit,
never WRANGLIT, never Wrang-lit. The Obsidian theme built from these tokens is
**Wranglitdark** — one word, capital W only.

Apply the casing from the first draft. Fixing it later is a re-render.

---

## 2. Colour

Two families only: one orange, one neutral. No second accent colour. If a design
needs a third colour, it needs a reason first.

### 2.1 Orange

Burnt orange. The accent, the brand, the active state. Never used to mean
"good" or "bad" — status has its own colours in §2.3.

| Token | Hex | Use |
|---|---|---|
| `--w-orange-50` | `#FFF4ED` | faintest tint, hover rows in light mode |
| `--w-orange-100` | `#FFE6D5` | selected row background, light mode |
| `--w-orange-200` | `#FFC9AA` | borders on tinted surfaces |
| `--w-orange-300` | `#FDA474` | decorative only, never type |
| `--w-orange-400` | `#FB7435` | **accent on dark surfaces** — icons, links, active marks |
| `--w-orange-500` | `#EA580C` | **the brand orange** — fills, chrome, the halo |
| `--w-orange-600` | `#C2410C` | UI text and links on white; hover/press on `500` |
| `--w-orange-700` | `#9A3412` | **body text and links on white**; text on pale orange tints |
| `--w-orange-800` | `#7C2D12` | pressed states on light surfaces |
| `--w-orange-900` | `#431407` | deepest tone, rarely needed |

### 2.2 Ink

The neutral spine. Near-black through to near-white.

| Token | Hex | Use |
|---|---|---|
| `--w-ink-950` | `#0C0C0E` | **the dark canvas** — editor background in dark mode |
| `--w-ink-900` | `#131316` | dark elevated surface |
| `--w-ink-800` | `#1C1C21` | **the dark chrome** — sidebar, ribbon, titlebar |
| `--w-ink-700` | `#26262D` | borders and dividers in dark mode |
| `--w-ink-600` | `#3A3A44` | disabled type on dark |
| `--w-ink-500` | `#55555F` | **muted text on white** |
| `--w-ink-400` | `#7A7A85` | placeholder, the one token that works on both |
| `--w-ink-300` | `#A5A5AE` | **muted text on dark** |
| `--w-ink-200` | `#CECED4` | borders and dividers in light mode |
| `--w-ink-100` | `#E7E7EA` | **body text on dark** |
| `--w-ink-50` | `#F5F5F7` | light secondary surface |
| `--w-white` | `#FFFFFF` | the light canvas, always |

### 2.3 Status

Status is never the brand orange. Orange is identity; these carry meaning.

| Meaning | Light fg | Light bg | Dark fg |
|---|---|---|---|
| OK | `#15803D` | `#DCFCE7` | `#4ADE80` |
| Warning | `#A16207` | `#FEF3C7` | `#FACC15` |
| Error | `#B91C1C` | `#FEE2E2` | `#F87171` |
| Info | `#1D4ED8` | `#DBEAFE` | `#60A5FA` |

### 2.4 Contrast — the rules that are not negotiable

Measured, not estimated. WCAG 2.2 AA is the floor; AAA where it was free.

| Pairing | Ratio | Verdict |
|---|---|---|
| `orange-700` on white | 7.31 | AAA — **use this for body links** |
| `orange-600` on white | 5.18 | AA — UI labels |
| `orange-500` on white | 3.56 | **FAILS normal text.** Fills and large display only |
| black `ink-950` on `orange-500` | 5.49 | AA — **text on an orange button is black** |
| white on `orange-500` | 3.56 | **FAILS. Never put white text on the brand orange** |
| `orange-400` on `ink-800` | 6.18 | AA — accent on the dark sidebar |
| `ink-100` on `ink-950` | 15.84 | AAA — dark-mode body |
| `ink-300` on `ink-950` | 8.00 | AAA — dark-mode muted |
| `ink-500` on white | 7.37 | AAA — light-mode muted |

Two rules fall out of that table and both are easy to get wrong:

1. **White text never goes on the brand orange.** Use `ink-950`. A white-on-orange
   button fails AA at every normal text size.
2. **The brand orange is never body text on white.** Step down to `orange-700`.

---

## 3. Type

System stack, no webfonts. A knowledge vault should not wait on a font request.

```
--w-font-ui:   -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--w-font-text: inherit from --w-font-ui;
--w-font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
```

| Role | Size | Weight | Line height |
|---|---|---|---|
| Display | 32px | 700 | 1.2 |
| H1 | 26px | 700 | 1.25 |
| H2 | 21px | 650 | 1.3 |
| H3 | 17px | 600 | 1.4 |
| Body | 16px | 400 | 1.6 |
| Small | 14px | 400 | 1.5 |
| Caption | 12px | 500 | 1.4 |

Headings are ink, never orange. Orange marks the *active* heading, not every one.

---

## 4. Spacing and shape

A 4px base. Every gap is a multiple of it.

```
--w-space-1: 4px    --w-space-4: 16px   --w-space-7: 40px
--w-space-2: 8px    --w-space-5: 24px   --w-space-8: 48px
--w-space-3: 12px   --w-space-6: 32px   --w-space-9: 64px
```

```
--w-radius-sm: 4px     --w-radius-lg: 12px
--w-radius-md: 8px     --w-radius-pill: 999px
```

Elevation is a border plus a soft shadow, never a heavy drop shadow.

```
--w-shadow-1: 0 1px 2px rgba(12,12,14,0.06);
--w-shadow-2: 0 2px 8px rgba(12,12,14,0.10);
--w-shadow-3: 0 8px 24px rgba(12,12,14,0.14);
```

---

## 5. Focus

A focus ring is an indicator, not decoration. It must be a real, visible outline
at 2px, in a colour that passes 3:1 against its surround.

```
light mode:  outline: 2px solid var(--w-orange-600);  outline-offset: 2px;
dark mode:   outline: 2px solid var(--w-orange-400);  outline-offset: 2px;
```

A border-colour swap is not a focus indicator — on a border-less control it is a
no-op. Use `outline`.

---

## 6. Voice

- Plain words. Short sentences. One idea per sentence.
- No em-dashes in UI copy or chat replies.
- Sentence case for headings and buttons. Not Title Case, not ALL CAPS.
- Buttons say what happens: "Create note", not "Submit".
- Never blame the user in an error. Say what went wrong and what fixes it.

See [[GL-008-plain-language-iso-24495-1]] for the full writing standard.

---

## 7. Charts

- One series: `orange-500` on light, `orange-400` on dark.
- Two to four series: step down the orange scale — `500`, `700`, `300`, `900`.
  Never introduce an unrelated hue to add a series.
- Five or more series: the chart is wrong. Split it or aggregate it.
- Never encode meaning in colour alone. Label directly on the mark.
- Gridlines are `ink-200` on light, `ink-700` on dark. Never black.

---

## 8. The geometry rule (for the Obsidian theme)

The Wranglitdark theme sets **colour, type and icons. It sets no geometry.**

Obsidian's `app.js` measures the file tree and writes the result back onto every
row as an inline `padding-inline-start: <n>px !important`. A layout declaration
anywhere in the sidebar chain poisons that measurement, and the indent compounds
by about 17px on every rebuild until the tree runs off the pane.

So never add to the theme, on any element in the sidebar or file-explorer chain:

```
padding  margin  position  top/left/right/bottom  width  height
min-width  max-width  display  flex  grid  transform  box-sizing
overflow  gap  inset  float  contain
--size-*  --nav-item-padding  --nav-item-children-*  --indent-size
--file-margins  --line-width  --sidebar-*  --header-height
```

Colour-valued variables that merely start with a layout-ish prefix are fine:
`--nav-item-color`, `--tab-background-active`, `--indentation-guide-color` change
no boxes.

A related trap: **never use `mask-image` on a container.** A mask clips everything
the element paints, children included — masking the file-tree container renders
the sidebar as an empty pane. If a graphic needs to tint per mode, bake the tint
into two `background-image` data URIs, one per mode.

---

## 9. Making it your own

This system is neutral on purpose. To rebrand:

1. Replace the ten orange values in §2.1 with your own scale.
2. **Re-run the contrast check.** Do not skip this. Rewrite the §2.4 table with
   your measured numbers, and re-derive which step is safe for body text and
   which colour goes on top of your brand fill. The two rules in §2.4 are
   specific to this orange; yours will differ.
3. Swap the same tokens in `.obsidian/themes/Wranglitdark/theme.css` — they are
   declared once at the top of that file.
4. Rename the theme folder and its `manifest.json` if you want your own name.
5. Tell Iris what changed. Iris updates this file; everyone else reads it.

Never edit the tokens in the theme CSS without editing them here. This file is
the source; the theme is a consumer.

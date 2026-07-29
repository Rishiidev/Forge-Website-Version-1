# GitHub PR Template — per-page PR body format

Every forge-bespoke page is its own branch and its own PR. The PR body is the craft evidence — before/after screenshots, the self-review checklist, and the design decisions the agent made on the way. This template is loaded by `scripts/build.py` when opening the PR.

The template lives at `templates/pr-body.md.tmpl` and renders with the per-page context.

---

## PR Title Format

```
feat(<page>): <business-slug> — <page-name>
```

Examples:
- `feat(index): de-bella-beau — home`
- `feat(services): de-bella-beau — services`
- `feat(cro): de-bella-beau — service-picker integration`

---

## PR Body Structure

```markdown
## Page: <page-name>

**Business:** <business-name>
**Industry:** <industry>
**CRO engine on this page:** <yes/no, type>
**Pre-flight gates passed:** <list>

## Screenshots

### Mobile (375×812)
![Mobile before](<link-to-before-screenshot>)
![Mobile after](<link-to-after-screenshot>)

### Desktop (1440×900)
![Desktop before](<link-to-before-screenshot>)
![Desktop after](<link-to-after-screenshot>)

## Design decisions

1. **<Decision 1>** — <what> chosen because <why>. Rejected: <alternatives>.
2. **<Decision 2>** — ...

## CRO engine integration (if applicable)

**Engine type:** <test-picker | mood-picker | service-picker | quote-builder | etc.>
**Data source:** <link to JSON or reference>
**State transitions verified:** <list>
**Screenshots of every state:** <links>

## Self-review checklist

- [ ] No fabricated content (reviews, hours, prices)
- [ ] No dead buttons (every CTA resolves)
- [ ] No placeholders visible
- [ ] No em-dashes, no AI tells
- [ ] Lighthouse ≥95 on all 4 axes (mobile)
- [ ] CRO engine works end-to-end
- [ ] Real photos with onerror fallback
- [ ] `prefers-reduced-motion` honored
- [ ] `prefers-color-scheme` respected
- [ ] One accent, one font pair, one radius (locked)
- [ ] WCAG AA contrast on all text
- [ ] Alt text on every meaningful image

## Pre-flight output

```
<paste of preflight.py output>
```

## Lighthouse report

```
<paste of lighthouse.py output — perf/a11y/best/SEO scores>
```

Full report: <link-to-lighthouse-json>

## Design references

- DESIGN.md (committed to main): <link>
- Industry playbook: <link>
- CRO engine spec: <link>

---

🤖 Generated with [forge-bespoke](https://github.com/Rishiidev/Forge-Website-Version-1)
```

---

## Branch Naming Convention

| Page | Branch |
|---|---|
| Home | `feat/index` |
| Services | `feat/services` |
| Reviews | `feat/reviews` |
| Contact | `feat/contact` |
| About | `feat/about` |
| CRO engine integration | `feat/cro-<engine-type>` |
| Design system setup | `feat/design-system` (merged first) |
| Lighthouse fixes | `chore/lighthouse` (after perf issues) |

---

## Commit Message Convention

Conventional Commits. Examples:

```
feat(index): add hero + trust bar + CRO engine

- Hero with one primary CTA (WhatsApp to Book)
- Trust bar above the fold with rating + count + city
- CRO engine (service-picker) within first two scrolls
- Self-host 3 hero photos, onerror fallback to monogram

Pre-flight: 12/12 gates pass
Lighthouse mobile: perf=98 a11y=100 best=100 seo=100
```

```
fix(services): resolve dead CTA on service card #3

Service card #3 had href="#" — replaced with wa.me/<digits>?
text=<pre-fill with service name>.

Pre-flight: 12/12 gates pass after fix.
```

```
chore(lighthouse): defer CRO engine script

The CRO engine script was render-blocking, dropping perf from 96 to 91.
Added `defer` attribute. Perf back to 97.

Pre-flight: 12/12 gates pass after fix.
```

---

## Merge Strategy

- **Squash merge** for trivial changes (typo fixes, link fixes).
- **Squash merge** for most page PRs (keeps main linear).
- **Merge commit** for the design-system PR (preserves the SETUP commit for posterity).
- **Auto-merge** is enabled — once the self-review is approved, the PR auto-merges when CI passes.

Branch protection on main:
- Require 1 approval (which is the agent's self-review)
- Require CI to pass (which is `preflight.py + lighthouse.py + cro_test.py`)
- No force-pushes

---

## The merge history as deliverable

The `git log --oneline` on main is the design history. Every commit is a craft decision. The client can read it like a changelog. Examples:

```
$ git log --oneline
a4f2e91 chore(lighthouse): defer CRO engine script
8b3c0dd feat(index): add hero + trust bar + CRO engine
2e9f7a1 feat(design): write DESIGN.md for de-bella-beau
1d4b6c2 chore(initial): scaffold repo + per-page branches
```

The merge history is the proof. Don't squash it. Don't `--no-verify` it. Don't merge without screenshots.
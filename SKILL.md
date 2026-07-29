---
name: forge-bespoke
description: Build a hand-crafted, Git-tracked, pre-flight-gated ₹24,999 Made-For-You website for a Forge prospect. Three input modes (PDF, Google My Business link, questionnaire). Per-page PR cycle with screenshots and self-review. Industry-specific CRO engine (test picker for clinic, mood picker for restaurant, service picker for salon, quote builder for everything else). Pre-flight refuses to ship fabricated content, dead buttons, placeholders, em-dashes, or any page scoring <95 on Lighthouse mobile. Output: live Vercel URL + GitHub repo with design history + WhatsApp handoff draft. The source of truth lives at https://github.com/Rishiidev/Forge-Website-Version-1.
---

# Forge Bespoke — the ₹24,999 Made-For-You engine

This skill produces **hand-crafted websites** for the Made-For-You tier. It's slower, more rigorous, and more expensive than `forge-website` (₹9,999 template) and `forge-website-pro` (₹24,999 template-fill). Three things make it different:

1. **Per-page PR cycle.** Every page is its own branch, its own PR, its own self-review, its own screenshot pair. The merge history is the evidence of craft.
2. **Pre-flight mechanical gates.** Zero em-dashes. Zero dead buttons. Zero placeholders. Lighthouse ≥95 on all 4 axes, mobile. Every gate is automated and a hard fail.
3. **Industry-specific CRO engine.** Test picker for clinic, mood picker for restaurant, service picker for salon, quote builder for everything else. The single biggest thing that earns the ₹15K delta.

The skills `impeccable` and `design-taste-frontend` run **inside my (Hermes) context** as the craft standard. They are **never** referenced from the shipped HTML/CSS/JS. The site is vanilla, owned by the client.

## When to invoke

- "build the made-for-you site", "build the 24,999 site", "ship the bespoke"
- After a prospect said YES to a `forge-positioning`-pitched Made-For-You quote
- Slash: `/forge-bespoke --from-gbp <url>`
- Slash: `/forge-bespoke --from-pdf <path>`
- Slash: `/forge-bespoke --from-questionnaire` (interactive walk)

Do NOT use for:
- ₹9,999 tier → use `forge-website`
- Template-fill ₹24,999 → use `forge-website-pro`
- The prospect is in pre-decision → use `forge-audit` first

## The workflow

```
1. INPUT GATE
   Accept: --from-gbp <url>  |  --from-pdf <path>  |  --from-questionnaire
   Reject if: no business signals, no phone/WhatsApp, no photos — refuse to build with missing data

2. EXTRACT SIGNALS → normalize to .client.json (same shape regardless of mode)

3. DESIGN READ + DIALS (design-taste-frontend)
   - Section 0.B one-liner: "Reading this as: <industry> for <ICP>, with <vibe>, leaning <system>"
   - Set 3 dials: VARIANCE / MOTION / DENSITY — explicit values, justified
   - Pick design system (real package or labeled aesthetic)
   - Lock accent + font pair + radius + grid
   - WRITE DESIGN.md — single source of truth (committed to the per-client repo)

4. PER-PAGE BUILD + PER-PAGE PR (loop 5x: home, services, reviews, contact, about)
   For each page:
     a. Create branch feat/<page>
     b. Build the page per templates + design system
     c. Integrate CRO engine if Home or Services
     d. Write CRO test cases (test-picker has 7 branches; verify each)
     e. Run preflight.py on the branch
     f. Run lighthouse.py on the page (fail if <95)
     g. Take mobile (375px) + desktop (1440px) screenshots
     h. Commit + push + open PR with screenshots
     i. Self-review via github-code-review checklist
     j. Only merge to main when all gates pass

5. FINAL preflight on main

6. DEPLOY to Vercel

7. WRITE <slug>--<date>.delivered.json with:
   - live URL
   - github repo URL (public, this is the design history)
   - list of commits + PRs
   - lighthouse scores per page
   - mobile + desktop screenshots
   - CRO engine test results

8. WHATSAPP HANDOFF: live URL + repo URL + "here's the design history" link
```

## The three input modes

| Mode | Script | Use when |
|---|---|---|
| **Mode 1: PDF** | `scripts/extract_from_pdf.py` | Client has a CV or portfolio PDF and no other web presence |
| **Mode 2: GBP** | `scripts/extract_from_gbp.py` | Client is a local business with a Google Maps listing (most common) |
| **Mode 3: Questionnaire** | `scripts/questionnaire.py` | Client has neither a PDF nor a GBP — or input is incomplete |

The questionnaire is structured (18 questions, branching logic, per-industry variants). Lives at `assets/questionnaire.json`. Loaded by `scripts/questionnaire.py`. Mode 3 walks one question per turn, conversational, never as a wall.

## The 7 industry-specific CRO engines

| Engine | Industries | What it does |
|---|---|---|
| `test-picker` | clinic, diagnostic-centre, dental, physio, vet | Pick a test → see fasting + sample + report timing + WhatsApp CTA pre-filled with the test name |
| `mood-picker` | restaurant, café | "What are you in the mood for?" → table size + time + occasion + book |
| `service-picker` | salon, beauty, spa | Pick a service + length → see matching slots + WhatsApp each |
| `project-picker` | contractor, plumber, electrician, AC, mechanic | Project-type + size + photo upload → quote + book site visit |
| `stock-check` | retail, boutique | "Is it in stock?" → yes/no + reserve CTA + WhatsApp |
| `class-picker` | fitness, gym, yoga, dance | Pick a class type → next 7-day schedule + WhatsApp confirmation |
| `quote-builder` | coach, tutor, consultant, B2B service | Problem → scope → WhatsApp handoff |

v1 ships 4 engines: `test-picker`, `mood-picker`, `service-picker`, `quote-builder`. The other 3 ship in v1.5.

## The 9 industry templates

| Template | ICP | Palette anchor | Font display | Primary CTA | CRO engine |
|---|---|---|---|---|---|
| `clinic` | ICP-1 | `#2c7a7b` soft teal | Source Serif 4 | WhatsApp to Enquire | test-picker |
| `salon` | ICP-1 | `#c97f3a` warm copper | Fraunces | WhatsApp to Book | service-picker |
| `restaurant` | ICP-2 | `#6b3410` warm espresso | Playfair Display | Reserve a Table | mood-picker |
| `contractor` | ICP-4 | `#1e3a5f` industrial blue | Inter (only) | Get a Free Quote | project-picker (v1.5) |
| `retail` | ICP-2 | `#5b1a1a` deep maroon | Instrument Serif | Check Stock | stock-check (v1.5) |
| `fitness` | ICP-2 | `#2b6e2b` lime | Space Grotesk | Book First Class Free | class-picker (v1.5) |
| `auto` | ICP-4 | `#cc4b1a` industrial orange | IBM Plex Sans | Get a Free Quote | project-picker (v1.5) |
| `coach` | ICP-3 | `#1a2332` deep navy | Fraunces | Book Free Discovery Call | quote-builder |
| `personal` | ICP-3 | n/a (per-client) | n/a | per-client | quote-builder |

v1 ships templates for: `clinic`, `salon`, `restaurant`, `coach`, `personal`. The other 5 ship in v1.5.

## The pre-flight gates (every one is a hard fail)

| Gate | Enforced by |
|---|---|
| No fabricated content (reviews, hours, prices) | `scripts/preflight.py` |
| No dead buttons (every CTA resolves) | `scripts/link_probe.py` |
| No placeholders visible (`{{TOKEN}}`, "Coming soon") | `scripts/preflight.py` |
| No em-dashes, no AI tells | `scripts/preflight.py` (regex sweep) |
| Lighthouse ≥95 mobile on all 4 axes | `scripts/lighthouse.py` |
| CRO engine works end-to-end | `scripts/cro_test.py` |
| Real photos with onerror fallback | `scripts/preflight.py` |
| `prefers-reduced-motion` honored | `scripts/accessibility.py` |
| `prefers-color-scheme` respected | `scripts/accessibility.py` |
| One accent, one font pair, one radius | `scripts/preflight.py` |

## The 5 pages

Every site ships exactly these 5 — the Made-For-You promise:

| Page | Purpose | Bespoke rules |
|---|---|---|
| `index.html` | Hero + trust + CRO engine + services + reviews + contact | One primary CTA. Trust bar above the fold. CRO engine within the first two scrolls. |
| `services.html` | Full list with per-item WhatsApp CTAs | Each service has its own pre-filled WhatsApp link. |
| `reviews.html` | Honest aggregate + leave-a-review CTA | Never invent quotes. Show the count + score + deep-link to read on Google. |
| `contact.html` | Action cards + map + hours | Direct action cards: WhatsApp / Call / Directions. Map iframe with 1.5s OSM safety net. Hours table that highlights today. |
| `about.html` | Story + hours + WhatsApp CTA | Skip unless audit flagged "no website" specifically. |

## GitHub deliverable (per-client repo)

Every build produces a **public GitHub repo** at `https://github.com/Rishiidev/<business>--site`. Contains:

1. The full site code (HTML/CSS/JS — vanilla, no proprietary dependencies)
2. `DESIGN.md` — the design read, the dials, the rationale, the rejected alternatives
3. The `git log --oneline` — every commit is a craft decision, screenshot-attached
4. The PR history — 5 PRs, one per page, each with before/after screenshots and a self-review
5. The Lighthouse report PDF
6. The accessibility audit (axe results + VoiceOver notes)
7. The CRO engine test report (every branch + WhatsApp pre-fill captured)

This is the artifact the ₹24,999 client takes home. It is the ₹15K price-delta justified by evidence.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | This file — the canonical spec |
| `README.md` | Human-facing repo overview |
| `package.json` | Skill manifest + version |
| `assets/questionnaire.json` | The 18-question conversational intake |
| `assets/industry-playbooks.json` | 7 CRO engines + per-industry defaults |
| `references/cro-engines.md` | Per-industry CRO engine specs |
| `references/design-systems.md` | Per-industry palette + font pair + rationale |
| `references/preflight-checklist.md` | The mechanical Section 14 gates |
| `references/lighthouse-targets.md` | Per-page perf/a11y/best/SEO budget |
| `references/github-pr-template.md` | Per-page PR body format |
| `references/tone-of-voice.md` | Honest-only copy rules |
| `templates/DESIGN.md.tmpl` | The design read + dials + system |
| `templates/pr-body.md.tmpl` | The PR description w/ screenshots + self-review |
| `templates/per-industry/<industry>/*` | 9 industry × 5 pages |
| `scripts/build.py` | Orchestrator |
| `scripts/preflight.py` | Mechanical gates |
| `scripts/cro_test.py` | CRO engine state-transition tests |
| `scripts/lighthouse.py` | Per-page Lighthouse runner |
| `scripts/screenshots.py` | cua-driver: 375px + 1440px |
| `scripts/accessibility.py` | axe-core + VoiceOver smoke |
| `scripts/link_probe.py` | Every CTA target verified |
| `scripts/extract_from_pdf.py` | Mode 1 |
| `scripts/extract_from_gbp.py` | Mode 2 |
| `scripts/questionnaire.py` | Mode 3 |

## Key invariants

1. **The skills run in me, not in the site.** `impeccable` and `design-taste-frontend` are loaded into my context. The shipped HTML/CSS/JS has zero references to them. Vanilla site, owned by the client.
2. **No fabricated content.** Reviews = GBP count + score only. Hours = GBP exactly. Prices = "Confirm by WhatsApp" if not public.
3. **No dead buttons.** Every CTA resolves to a working target verified by `link_probe.py`.
4. **No placeholders.** `{{TOKEN}}` never ships. "Coming soon" never ships. `Lorem ipsum` never ships.
5. **No em-dashes, no AI tells.** Pre-flight regex sweep hard-fails the build on any `—`, any "Elevate," "Seamless," "Quietly trusted by."
6. **Lighthouse ≥95 mobile on all 4 axes.** Build fails loud if any page misses.
7. **CRO engine works end-to-end.** Every state-transition tested. Every WhatsApp pre-fill captured.
8. **Real photos, with fallback.** Self-hosted. `onerror` swap to branded monogram.
9. **One accent, one font pair, one radius.** Per `design-taste-frontend` Sections 4.2 / 4.4.
10. **The per-client repo is public.** The design history is the proof of craft.

## Pitfalls

### P0. Plan first, get approval, then execute (carried forward from forge-website-pro)

Already done. This SKILL.md is the approved plan.

### P1. Skills in me, not in the site

The temptation in "bespoke" mode is to bake the `impeccable` craft standard into the shipped product — custom CSS framework, design system runtime, etc. Resist. The skills are my quality compass during build. The output is plain HTML/CSS/JS. The client owns the site and never needs Hermes to run it.

### P2. Bespoke ≠ gratuitously different

The temptation is to over-design — 3 fonts, 6 brand colors, custom cursors, animated SVG dividers. Resist. One accent, two fonts (display + body), one radius. The design system table in `references/design-systems.md` is the floor. The brief justifies going past it.

### P3. The questionnaire is a fallback, not the default

Mode 3 (questionnaire) is for when GBP or PDF doesn't exist. Most clients will be Mode 2 (GBP). The questionnaire walks one question per turn, never as a wall. If a question can be inferred from another answer, skip it.

### P4. The CRO engine is the heart, not a feature

The biggest mistake is treating the CRO engine as decoration. Test picker must have ≥10 real tests with real fields. Service picker must have ≥6 real services with real lengths. Mood picker must have ≥4 real occasions with real table sizes. Quote builder must produce a real WhatsApp pre-fill that the prospect can actually send. If the engine doesn't earn its place in the first 5 seconds of interaction, drop it.

### P5. Lighthouse ≥95 is hard on Indian hosting

The realistic target is 95-98 on perf, 95-100 on a11y/best/SEO. Mitigation: Vercel CDN + Cloudflare in front. Static-only sites. Self-hosted images at ≤100KB each. If the budget is missed, the gate fails — fix the cause (image weight, render-blocking CSS, missing alt text) before shipping.

### P6. The GitHub repo is the deliverable, not a side-effect

Every commit is a craft decision. Every PR is a self-review with screenshots. The merge history is the evidence of craft the client takes home. Don't merge with `--no-verify`. Don't squash the PR history. The repo IS the proof.

## See also

- `forge-audit` — produces the `.client.json` this skill consumes
- `forge-website` — the base ₹9,999 templated site
- `forge-website-pro` — the template-fill ₹24,999 site
- `forge-positioning` — ICP + tier naming + industry templates
- `impeccable` — the craft compass loaded into Hermes during build
- `design-taste-frontend` — the dials + design system + anti-slop loaded into Hermes during build
- `github-pr-workflow` — branch, commit, PR, merge, CI
- `github-code-review` — the pre-merge self-review checklist
- `github-repo-management` — per-client repo creation + branch protection

## Source

This skill's source of truth: https://github.com/Rishiidev/Forge-Website-Version-1
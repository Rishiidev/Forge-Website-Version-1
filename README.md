# Forge Website Version 1 — the Made-For-You ₹24,999 engine

> Hand-crafted 5-page websites with industry-specific CRO engines, Git-tracked per-page PR cycles, and pre-flight mechanical gates.

This is the source-of-truth repo for the `forge-bespoke` Hermes skill. The skill's `SKILL.md` lives in this repo and is loaded into Hermes from the local path `~/.hermes/skills/forge/bespoke/`.

## What this is

A builder that produces **bespoke ₹24,999 "Made-For-You" websites** for Indian SMBs. Different from `forge-website` (₹9,999 templated) and `forge-website-pro` (₹24,999 template-fill) in three concrete ways:

1. **Per-page PR cycle.** Every page is its own branch, its own PR, its own self-review, its own screenshot pair. The merge history is the evidence of craft.
2. **Pre-flight mechanical gates.** Zero em-dashes. Zero dead buttons. Zero placeholders. Lighthouse ≥95 on all 4 axes, mobile. Every gate is automated.
3. **Industry-specific CRO engines.** Not a generic quote-builder — a test picker for clinics, a mood picker for restaurants, a service picker for salons, a quote-builder for everything else. The single biggest thing that earns the ₹15K delta over the ₹9,999 tier.

## Architecture

```
impeccable + design-taste-frontend  ──►  my (Hermes) craft standard
                                          │
                                          ▼
forge-bespoke  ──►  orchestrator (build.py)
                       │
                       ├─► Mode 1: PDF / CV → personal-brand site
                       ├─► Mode 2: Google My Business link → 5-page local-business site
                       └─► Mode 3: questionnaire → fallback for neither PDF nor GBP
                                          │
                                          ▼
                       ┌──────── per-page PR cycle ────────┐
                       │                                    │
                       ▼                                    ▼
              1 industry template                1 industry-specific
              × 5 pages                          CRO engine
                       │                                    │
                       └──────── pre-flight ────────────────┘
                                          │
                                          ▼
                                  GitHub repo
                              + Vercel live URL
                          + WhatsApp handoff draft
```

The skills (`impeccable`, `design-taste-frontend`) run **inside the agent's context** as the craft standard. They are **never** referenced from the shipped HTML/CSS/JS. The site is vanilla, owned by the client.

## Three input modes

| Mode | When | Script |
|---|---|---|
| **PDF / Resume / CV** | Client has a CV or portfolio PDF and no other web presence | `scripts/extract_from_pdf.py` |
| **Google My Business link** | Client is a local business with a GBP listing | `scripts/extract_from_gbp.py` |
| **Questionnaire** | Client has neither a PDF nor a GBP — or input is incomplete | `scripts/questionnaire.py` |

## Repo structure

```
Forge-Website-Version-1/
├── README.md                       (this file)
├── LICENSE                         (MIT)
├── SKILL.md                        (canonical skill spec, loaded into Hermes)
├── package.json                    (skill manifest + version)
├── assets/
│   ├── questionnaire.json          (the 18-question conversational intake)
│   ├── industry-playbooks.json     (7 CRO engines + per-industry defaults)
│   └── logo/forge-mark.svg         (the Forge mark)
├── references/
│   ├── cro-engines.md              (per-industry CRO engine specs)
│   ├── design-systems.md           (per-industry palette + font pair + rationale)
│   ├── preflight-checklist.md      (mechanical Section 14 gates)
│   ├── lighthouse-targets.md       (per-page perf/a11y/best/SEO budget)
│   ├── github-pr-template.md       (per-page PR body format)
│   └── tone-of-voice.md            (honest-only copy rules)
├── templates/
│   ├── DESIGN.md.tmpl              (the design read + dials + system — written FIRST)
│   ├── pr-body.md.tmpl             (the PR description w/ screenshots + self-review)
│   └── per-industry/
│       ├── clinic/    (diagnostic centre, medical, dental, physio, vet)
│       ├── salon/     (hair, beauty, nail, spa)
│       ├── restaurant/(café, restaurant, food, bakery)
│       ├── contractor/(plumber, electrician, AC, mechanic, garage)
│       ├── retail/    (boutique, store, shop)
│       ├── fitness/   (gym, yoga, dance, martial arts)
│       ├── auto/      (auto service, body shop, tire)
│       ├── coach/     (coach, tutor, consultant)
│       └── personal/  (freelancer, professional, portfolio)
└── scripts/
    ├── build.py                    (orchestrator: input → repo → per-page PRs → merge → pre-flight)
    ├── preflight.py                (mechanical gates)
    ├── cro_test.py                 (every CRO engine state-transition + WhatsApp pre-fill)
    ├── lighthouse.py               (per-page Lighthouse runner, fails if <95 on any axis)
    ├── screenshots.py              (cua-driver: 375px mobile + 1440px desktop)
    ├── accessibility.py            (axe-core + VoiceOver smoke)
    ├── link_probe.py               (every CTA target verified)
    ├── extract_from_pdf.py         (Mode 1)
    ├── extract_from_gbp.py         (Mode 2)
    └── questionnaire.py            (Mode 3)
```

## The gates (what the pre-flight refuses to ship)

| Gate | What fails the build |
|---|---|
| **No fabricated content** | Reviews = GBP count + score only. Hours = GBP exactly. No invented prices. |
| **No dead buttons** | Every CTA resolves to a working target: wa.me/<digits>, tel:<digits>, mailto:, anchor with `id`, or external URL returning 2xx. |
| **No placeholders visible** | No `{{TOKEN}}` ships. No "Coming soon." No `Lorem ipsum`. |
| **No em-dashes, no AI tells** | Pre-flight regex sweep: zero `—`, zero `–`, zero "Elevate," "Seamless," "Quietly trusted by," etc. |
| **Lighthouse ≥95 on all 4 axes, mobile** | Build fails if any page scores <95 on perf, a11y, best-practices, or SEO at mobile emulation. |
| **CRO engine works end-to-end** | `cro_test.py` exercises every state-transition. Every WhatsApp CTA fires the correct pre-filled message. |
| **Real photos only, with fallback** | All photos self-hosted. Every `<img>` has `onerror` swap to a branded monogram. |
| **prefers-reduced-motion honored** | Motion > `MOTION_INTENSITY: 3` is gated behind `@media (prefers-reduced-motion: no-preference)`. |
| **prefers-color-scheme respected** | Dual-mode tested. Theme locked. No mid-page section flips. |
| **One accent, one font pair, one radius** | Per `design-taste-frontend` Section 4.2 / 4.4. Lock enforced in `preflight.py`. |

## License

MIT — use, fork, learn from.
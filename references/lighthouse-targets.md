# Lighthouse Targets — the per-page performance budget

Every forge-bespoke page is held to these targets. Measured at mobile emulation (375×812, 4G throttling, 4x CPU slowdown). The targets are realistic for static-only sites with self-hosted assets on Vercel + Cloudflare. If a page misses the budget, `scripts/lighthouse.py` fails loud and the build stops.

---

## Per-page targets

| Page | Perf | A11y | Best | SEO | Notes |
|---|---|---|---|---|---|
| `index.html` | ≥95 | ≥95 | ≥95 | ≥95 | The home page is the highest-stakes — must score ≥95 on all 4 axes. |
| `services.html` | ≥95 | ≥95 | ≥95 | ≥95 | |
| `reviews.html` | ≥95 | ≥95 | ≥95 | ≥95 | |
| `contact.html` | ≥95 | ≥95 | ≥95 | ≥95 | The map iframe is a risk to perf — load lazily + 1.5s safety net. |
| `about.html` | ≥95 | ≥95 | ≥95 | ≥95 | |

If a page ships a CRO engine, the script loads deferred (`defer` attribute, never `async`). The script size budget is ≤15 KB minified per engine. Anything larger is a fail.

---

## Core Web Vitals targets

| Metric | Target | Why |
|---|---|---|
| **LCP** (Largest Contentful Paint) | ≤2.5s | Above-the-fold hero image + headline rendered |
| **INP** (Interaction to Next Paint) | ≤200ms | CRO engine clicks should feel instant |
| **CLS** (Cumulative Layout Shift) | ≤0.1 | No layout jump as images / fonts load |
| **TBT** (Total Blocking Time) | ≤200ms | No long JS tasks on main thread |
| **Speed Index** | ≤3.0s | Visual completeness threshold |

---

## Image budget

| Asset | Max size | Format | Notes |
|---|---|---|---|
| Hero photo | 80 KB | WebP | Self-hosted, lazy-loaded if below fold |
| Gallery photo | 50 KB each | WebP | Self-hosted, lazy-loaded |
| Logo (SVG) | 4 KB | SVG | Inline if small |
| Monogram fallback (SVG) | 1 KB | SVG | Always inline |
| Favicon | 4 KB | ICO + SVG | Self-hosted |

If an image exceeds budget, run through `cwebp -q 80` and re-measure. If still over budget, the source photo is wrong — request a smaller version from the client.

---

## Font budget

- **Display font:** load only the weights used (400, 600 max). Self-host, never `<link>` Google Fonts.
- **Body font:** load only the weights used (400, 500 max). Self-host.
- **Total font payload:** ≤80 KB across all weights.
- **Strategy:** `font-display: swap`. No FOIT (flash of invisible text).

---

## JS budget

- **CRO engine script:** ≤15 KB minified per engine
- **Open-now indicator:** ≤2 KB (shows "Open now" / "Closed" based on GBP hours)
- **Mobile CTA bar:** ≤1 KB (sticky WhatsApp + Call on ≤768px)
- **Total inline + external JS:** ≤20 KB per page

If a CRO engine exceeds 15 KB, it's a fail. The engines are intentionally simple — vanilla JS, no deps, no animation libraries.

---

## CSS budget

- **Per-page CSS:** ≤20 KB unminified (≤8 KB minified + gzipped)
- **Inline critical CSS:** ≤5 KB (above-the-fold only)
- **CSS variables for tokens:** ≤2 KB

---

## Hosting targets

- **TTFB:** ≤200ms (Vercel edge + Cloudflare proxy)
- **HTML payload:** ≤30 KB per page
- **Total page weight:** ≤300 KB (mobile)

If hosting misses these, the gate fails — fix the cause (image weight, render-blocking CSS, hosting region) before shipping.

---

## How the Lighthouse runner works

```bash
python3 scripts/lighthouse.py \
  --url "https://<business>.vercel.app/" \
  --pages index services reviews contact about \
  --form-factor mobile \
  --output dist/lighthouse/
```

For each page, the script:

1. Runs `lighthouse <url> --form-factor=mobile --quiet --chrome-flags="--headless"`
2. Parses the JSON report
3. Asserts each axis ≥95
4. Writes `dist/lighthouse/<page>.json` (full report) and `dist/lighthouse/<page>.html` (visual)
5. Fails loud on any miss

Reports are committed to the per-client repo at `lighthouse/<page>.json` so the client can audit them.

---

## Realistic expectations

For an Indian SMB site (clinic / salon / restaurant / etc.):

- **Perf:** 95-98 typical. 99+ requires no images in the hero (rare for these clients).
- **A11y:** 95-100 typical. The pre-flight gates handle this.
- **Best-practices:** 95-100 typical.
- **SEO:** 100 typical. LocalBusiness JSON-LD + meta + OG + sitemap.

If perf <95, the usual causes in priority order:
1. Hero image >80 KB — re-encode at 80% WebP quality
2. Render-blocking Google Fonts — self-host with `<link rel="preload">`
3. Map iframe above the fold — move below the fold or lazy-load
4. CRO engine script not deferred — add `defer` attribute
5. Unused CSS — purge

The lighthouse runner surfaces the top 3-5 opportunities in the failure message.
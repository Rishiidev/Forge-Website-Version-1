# Pre-flight Checklist — the mechanical gates

Every forge-bespoke build runs `scripts/preflight.py` before merging any page to main and again on the final main before deploy. This document is the spec. Every gate is a hard fail.

The pre-flight mirrors `impeccable`'s Section 14, plus the bespoke-specific gates from this skill's SKILL.md.

---

## Gate 1: No fabricated content

**Enforced by:** `scripts/preflight.py --check=fabricated`

**Rule:** No invented reviews, hours, prices, claims, or stats.

| Check | How |
|---|---|
| Reviews must be GBP-sourced | Every testimonial block has `data-source="gbp"` or `data-source="client-confirmed"`. Quotes are verbatim from source. |
| Hours must match GBP | Every hour string matches a GBP hour, character-for-character (after lowercase normalization). |
| Prices must be sourced | Every price has `data-source="public-list"` or `data-source="confirm-by-whatsapp"`. "Confirm by WhatsApp" is an acceptable value — never invent a price. |
| Stats must be sourced | Every "X reviews" or "4.6 ★" must come from GBP. No round numbers without source. |

**Fail message:** "Gate 1 (no-fabricated): <file>:<line> — Review quote not sourced from GBP. Either remove or add data-source attribute."

---

## Gate 2: No dead buttons

**Enforced by:** `scripts/link_probe.py`

**Rule:** Every `<a class="btn">` and every `<button>` (when used as a CTA, not a form input) must resolve to a working target.

| CTA type | Acceptable targets |
|---|---|
| WhatsApp | `https://wa.me/<digits>` where `<digits>` is a real international number (no `?text=` empty body — pre-fill message required) |
| Call | `tel:<digits>` with a real number |
| Email | `mailto:<email>` with a real address |
| Anchor | `<href="#<id>">` where `<id>` exists in the page |
| External | `https://...` returning 2xx (verified by HEAD request) |
| Booking | Real booking URL returning 2xx |

**Disallowed:** `href="#"`, `href="javascript:void(0)"`, `href=""`, `href="javascript:;"`, `href="<placeholder>"`.

**Fail message:** "Gate 2 (no-dead-buttons): <file>:<line> — CTA href '<href>' is not in the acceptable target list."

---

## Gate 3: No placeholders visible

**Enforced by:** `scripts/preflight.py --check=placeholders`

**Rule:** No `{{TOKEN}}`, "Coming soon", "Lorem ipsum", "TODO", "TBD" ships in any rendered HTML.

```bash
grep -rE '\{\{[A-Z_]+\}\}' dist/    # Must return 0
grep -rE 'Coming soon|coming soon|Lorem ipsum|TODO|FIXME|TBD' dist/  # Must return 0
```

**Fail message:** "Gate 3 (no-placeholders): <file> — found literal '{{TOKEN}}' in shipped HTML."

---

## Gate 4: No em-dashes, no AI tells

**Enforced by:** `scripts/preflight.py --check=ai-tells`

**Rule:** Zero em-dashes (`—`), zero en-dashes-as-separators (`–`), zero AI-tell vocabulary.

```bash
grep -rnE '—|–' dist/                                  # Must return 0
grep -irnE '\b(Elevate|Seamless|Unleash|Next-Gen|Revolutionize|Quietly trusted by|Crafted with care|Game-changing|Cutting-edge|Best-in-class|World-class|In today.s fast-paced)\b' dist/  # Must return 0
```

**Note:** Date ranges use `-` (hyphen), not `–` (en-dash). Number ranges use `-` (hyphen), not `–`.

**Fail message:** "Gate 4 (no-ai-tells): <file>:<line> — found em-dash. Replace with hyphen, period, or restructure sentence."

---

## Gate 5: Lighthouse ≥95 on all 4 axes (mobile)

**Enforced by:** `scripts/lighthouse.py`

**Rule:** Every page scores ≥95 on performance, accessibility, best-practices, and SEO at mobile emulation.

```bash
lighthouse <url> --form-factor=mobile --quiet --chrome-flags="--headless" \
  --output=json --output-path=<report>
python3 -c "
import json
r = json.load(open('<report>'))
for k in ['performance', 'accessibility', 'best-practices', 'seo']:
    score = r['categories'][k]['score'] * 100
    if score < 95:
        print(f'FAIL: {k}={score}')
        exit(1)
"
```

**Fail message:** "Gate 5 (lighthouse): <page> — performance=87 (need ≥95). Run lighthouse with --view to diagnose."

---

## Gate 6: CRO engine works end-to-end

**Enforced by:** `scripts/cro_test.py`

**Rule:** Every state-transition in the CRO engine works. Every WhatsApp CTA fires the correct pre-filled message. Screenshots captured of every state.

```python
# For each engine type, for each state-transition:
#   1. Headless browser navigates to the page
#   2. Performs the action (click, type, pick)
#   3. Asserts the expected state-change
#   4. Asserts the WhatsApp CTA href contains the correct pre-fill text
#   5. Screenshots the resulting state to dist/cro-tests/<page>/<state>.png
```

**Fail message:** "Gate 6 (cro-engine): test-picker — picking 'CBC' did not produce the expected details panel. Expected selector '.cro-engine__detail' to be visible."

---

## Gate 7: Real photos with onerror fallback

**Enforced by:** `scripts/preflight.py --check=photos`

**Rule:** Every `<img>` has a real `src` (not a placeholder URL), a meaningful `alt`, and an `onerror` handler that swaps to a branded monogram.

```bash
grep -rnE '<img[^>]*src="https?://[^"]+"' dist/ | grep -v 'onerror'    # Must return 0
```

**Acceptable:** `<img src="./assets/images/photo.webp" alt="..." onerror="this.onerror=null;this.src='./assets/images/monogram.svg';">`

**Fail message:** "Gate 7 (photos): <file>:<line> — `<img>` has no `onerror` fallback. Self-host the photo or add the fallback."

---

## Gate 8: prefers-reduced-motion honored

**Enforced by:** `scripts/accessibility.py`

**Rule:** Any motion above `MOTION_INTENSITY: 3` is gated behind `@media (prefers-reduced-motion: no-preference)`. CSS `animation` and `transition` properties without a reduced-motion gate are a fail when the motion dial is above 3.

```bash
# Check 1: no infinite-loop animations
grep -rnE 'animation:.*infinite' dist/*.css | grep -v 'prefers-reduced-motion'   # Must return 0

# Check 2: no transform: translate / scale in keyframes without reduced-motion gate
grep -rnE '@keyframes' dist/*.css | grep -v 'prefers-reduced-motion'              # Must return 0 if motion > 3
```

**Fail message:** "Gate 8 (reduced-motion): <file>:<line> — animation without reduced-motion gate. Wrap in @media (prefers-reduced-motion: no-preference)."

---

## Gate 9: prefers-color-scheme respected

**Enforced by:** `scripts/accessibility.py`

**Rule:** Page-level theme is locked. Sections do not flip between light and dark mid-page. Both light and dark tokens are defined. `prefers-color-scheme` is respected unless the brand insists on one mode.

**Visual check:** Take screenshots at light and dark mode. The site should look complete and on-brand in both modes.

**Fail message:** "Gate 9 (color-scheme): section 7 inverts theme mid-page. Pick one theme for the page."

---

## Gate 10: One accent, one font pair, one radius

**Enforced by:** `scripts/preflight.py --check=design-system`

**Rule:** Per `design-taste-frontend` Sections 4.2 / 4.4. Audit:

```bash
# Count distinct hex colors used as accents (everything matching --accent-pattern)
grep -oE '#[0-9a-f]{6}' dist/*.css | sort -u | wc -l

# Count distinct font-family declarations
grep -oE 'font-family:[^;]+' dist/*.css | sort -u | wc -l

# Count distinct border-radius values
grep -oE 'border-radius:[^;]+' dist/*.css | sort -u | wc -l
```

**Limits:** accent colors ≤ 1 (plus neutral palette), font families ≤ 2 (display + body), border-radius values ≤ 3 (small / medium / large within the locked scale).

**Fail message:** "Gate 10 (design-system): found 4 distinct accent colors. Lock to 1 accent + neutral palette."

---

## Gate 11: WCAG AA contrast on all text

**Enforced by:** `scripts/accessibility.py`

**Rule:** Every text element passes WCAG AA contrast against its background.

- Body text: ≥4.5:1
- Large text (18px+ or 14px+ bold): ≥3:1

**Fail message:** "Gate 11 (contrast): <file>:<line> — text color `#888` on background `#fff` is 3.5:1 (need 4.5:1). Darken text or change background."

---

## Gate 12: Alt text on every meaningful image

**Enforced by:** `scripts/preflight.py --check=alt`

**Rule:** Every `<img>` has non-empty `alt`. Decorative images have `alt=""`.

```bash
grep -rnE '<img[^>]*(?<!alt=)[^>]*>' dist/*.html | grep -v 'alt='   # Must return 0
```

**Fail message:** "Gate 12 (alt): <file>:<line> — `<img>` missing alt attribute."

---

## How the pre-flight runs

```bash
# Per-page (on the feat/<page> branch, before merge)
python3 scripts/preflight.py --target=dist/<page>/ --strict

# On main, after all 5 pages merged, before deploy
python3 scripts/preflight.py --target=dist/ --strict
```

The `--strict` flag turns every warning into an error. There is no `--lenient` mode in production. Build fails loud on any gate failure.

---

## Output

On success:

```
✓ Gate 1: no-fabricated (5 files checked, 0 issues)
✓ Gate 2: no-dead-buttons (12 CTAs checked, 12 verified)
✓ Gate 3: no-placeholders (5 files checked, 0 issues)
✓ Gate 4: no-ai-tells (5 files checked, 0 issues)
✓ Gate 5: lighthouse (5/5 pages ≥95 on all axes)
✓ Gate 6: cro-engine (test-picker: 8/8 state-transitions verified)
✓ Gate 7: photos (24/24 images have onerror fallback)
✓ Gate 8: reduced-motion (motion gated correctly)
✓ Gate 9: color-scheme (locked theme verified)
✓ Gate 10: design-system (1 accent, 2 fonts, 3 radii — locked)
✓ Gate 11: contrast (all text passes WCAG AA)
✓ Gate 12: alt (all images have alt)

Pre-flight: PASSED.
```

On failure:

```
✗ Gate 4: no-ai-tells
  dist/services.html:42 — found em-dash in "Hair colour that lasts — until next appointment"
  Suggestion: replace with period, comma, or restructure sentence.

Pre-flight: FAILED.
Build cannot continue. Fix and re-run.
```
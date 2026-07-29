# Design Systems — per-industry palette, font pair, and rationale

Every forge-bespoke site gets a **unique design system**. The skill picks it from this table based on the prospect's industry, not from a global default. These are **defaults, not rules** — the brief justifies overriding.

The principle: **one accent, two fonts (display + body), one radius**. The temptation in "bespoke" mode is to over-design — 3 fonts, 6 brand colors, custom cursors, animated SVG dividers. Resist.

---

## The 9 industry defaults

### 1. Clinic & Medical

- **Palette:** soft teal `#2c7a7b` on white `#fdfcf9`
- **Font pair:** Source Serif 4 (display) + Inter (body)
- **Mood:** calm, clinical, trustworthy
- **Why:** Teal is medical-by-association without the cliché of medical-cross blue. Source Serif 4 reads as authoritative without being old-fashioned. Inter for body is universally legible at body sizes.
- **Variance / motion / density:** 5 / 3 / 3

### 2. Salon & Beauty

- **Palette:** warm copper `#c97f3a` on cream `#faf6f1`
- **Font pair:** Fraunces (display) + Inter (body)
- **Mood:** editorial, premium, considered
- **Why:** Copper reads warm without the "salon pink" cliché. Fraunces has a contemporary editorial voice that reads premium without being cold. Cream neutral avoids the bright-white salon look.
- **Variance / motion / density:** 7 / 5 / 3

### 3. Café & Restaurant

- **Palette:** warm espresso `#6b3410` on cream `#f7f1e8`
- **Font pair:** Playfair Display (display) + Inter (body)
- **Mood:** local, considered, slow-food
- **Why:** Espresso brown reads food-by-association without being corporate. Playfair Display is editorial-classic. Cream neutral feels handmade vs. glossy.
- **Variance / motion / density:** 7 / 5 / 3

### 4. Service & Trade (contractor, plumber, electrician)

- **Palette:** industrial blue `#1e3a5f` on off-white `#fbfaf8`
- **Font pair:** Inter only (display + body — bold weights)
- **Mood:** solid, professional, no-nonsense
- **Why:** Industrial blue reads trade-by-association. Inter is the most legible at small sizes — important for service info (hours, service areas, pricing). One font keeps the design disciplined.
- **Variance / motion / density:** 4 / 3 / 4

### 5. Retail & Boutique

- **Palette:** deep maroon `#5b1a1a` on off-white `#fbf7f4`
- **Font pair:** Instrument Serif (display) + Inter (body)
- **Mood:** curated, considered, anti-amazon
- **Why:** Maroon reads boutique-by-association. Instrument Serif is editorial-modern — pairs well with maroon without feeling old. Off-white neutral is quieter than cream.
- **Variance / motion / density:** 6 / 4 / 3

### 6. Fitness & Studio

- **Palette:** lime `#2b6e2b` on warm white `#fafaf7`
- **Font pair:** Space Grotesk (display) + Inter (body)
- **Mood:** active, energetic, no-time-to-read
- **Why:** Lime reads fitness-by-association without the cliché of fitness-orange. Space Grotesk has a contemporary engineering voice. The body stays Inter for legibility.
- **Variance / motion / density:** 8 / 7 / 4

### 7. Auto & Trade

- **Palette:** industrial orange `#cc4b1a` on off-white `#fbfaf8`
- **Font pair:** IBM Plex Sans (display + body)
- **Mood:** honest, trade-grade, not showy
- **Why:** Industrial orange reads auto-by-association. IBM Plex Sans is engineering-by-association — fits trade service. Single font, like contractor.
- **Variance / motion / density:** 4 / 3 / 5

### 8. Coach & Tutor & Consultant

- **Palette:** deep navy `#1a2332` on warm white `#fafaf7`
- **Font pair:** Fraunces (display) + Inter (body)
- **Mood:** considered, evidence-first, calm authority
- **Why:** Deep navy reads professional-without-being-corporate. Fraunces gives the right amount of editorial weight for thought-leadership. Warm white keeps it from feeling cold.
- **Variance / motion / density:** 6 / 4 / 4

### 9. Personal Brand & Portfolio

- **Palette:** per-client (extracted from PDF)
- **Font pair:** per-client (extracted from PDF)
- **Mood:** per-client
- **Why:** Personal brands have a brand book or at least a colour preference. The PDF extractor pulls these. If no source, default to a clean editorial system (off-white + ink + single accent).
- **Variance / motion / density:** 7 / 5 / 3

---

## When to override

The brief wins. Override the defaults when:

1. The prospect has a brand book — use their colours + fonts.
2. The prospect mentioned a specific aesthetic — "editorial", "Linear-style", "Awwwards", "Apple-y".
3. The design read disagrees with the default — e.g. an upscale salon that wants monochrome + chrome, not warm copper.
4. The previous build of this industry used this exact palette — rotate to avoid brand-fatigue across deliveries.

Document the override in `DESIGN.md` with the rejected alternatives.

---

## Anti-patterns (from design-taste-frontend Section 4.2)

**Banned as defaults across all 9 industries:**

- AI-purple / blue-glow gradients
- Warm beige + brass + oxblood + ochre + espresso dark text (the AI-default premium-consumer palette)
- Fraunces or Instrument Serif when the brief is genuinely editorial / luxury / publication — rotate from the pool below

**Permitted serif pool** (when a serif is justified, rotate — don't reuse):

PP Editorial New, GT Sectra Display, Cardinal Grotesque, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, IvyPresto, Migra, Editorial Old, Saol Display, Söhne Breit Kursiv, Domaine Display, Canela, Schnyder, Tobias, NB Architekt, ITC Galliard.

---

## Colour consistency lock

Once an accent colour is chosen for a page, it is used on the **whole page**. A warm-grey site does not suddenly get a blue CTA in section 7. A rose-accented site does not get a teal status badge in the footer. Pick one accent, lock it, audit every component before shipping.

---

## Shape consistency lock

Pick ONE corner-radius scale for the page and stick to it:

- All-sharp (radius 0)
- All-soft (radius 12-16px)
- All-pill (full radius for interactive)

Mixed systems are allowed only when there is a documented rule (e.g. "buttons are full-pill, cards are 16px, inputs are 8px") and that rule is followed everywhere. Round buttons in a square layout, or square cards on a pill-button page, is broken design.

---

## Dark mode

Each design system ships with both light and dark tokens. Theme locked at the page level. Sections do not invert. `prefers-color-scheme` is respected by default unless the brand insists on one mode.

---

## The DESIGN.md output

Every forge-bespoke build writes a `DESIGN.md` to the per-client repo before any HTML is written. The structure is documented in `templates/DESIGN.md.tmpl`.
# Tone of Voice — honest-only copy rules

Every forge-bespoke site uses the same copy discipline. The principle: **say what is true, in the words the prospect understands, in the way a real person would say it.** No AI tells. No fabricated content. No corporate filler.

The hard rules below are enforced by `scripts/preflight.py`. The softer rules are craft standards followed by every copy decision.

---

## Hard rules (pre-flight enforced)

### 1. No fabricated content

| Don't | Do |
|---|---|
| "Trusted by 10,000+ customers" | "187 Google reviews, 4.6 average" (real number from GBP) |
| "Award-winning service" | "—" (skip if you can't cite the award) |
| "India's leading diagnostic centre" | "—" (skip if unprovable) |
| "Our happy customers" with invented quotes | The actual GBP review count + a "leave a review" CTA |
| "Open 24/7" when GBP says "Mon-Sat 9-7" | The exact GBP hours |

**The rule:** if you can't cite the source, don't write the claim. "Confirm by WhatsApp" is an acceptable value for any price not publicly listed.

### 2. No AI tells

| Don't | Do |
|---|---|
| "Elevate your experience" | "—" |
| "Seamless booking" | "WhatsApp to book. Replies in 10 minutes." |
| "Unleash your potential" | "—" |
| "Next-generation platform" | "—" |
| "Revolutionary approach" | "—" |
| "Crafted with care" | "—" |
| "Game-changing" | "—" |
| "Cutting-edge" | "—" |
| "Best-in-class" | "—" |
| "World-class" | "—" |
| "Quietly trusted by" | "—" or just "Trusted by" |
| "In today's fast-paced world" | "—" (delete the whole sentence) |
| "We are passionate about" | "We do X for Y." |

### 3. No em-dashes

Em-dashes (`—`) are banned in headlines, body copy, button text, captions, alt text, and quotes. Use:
- A period (`.`)
- A comma (`,`)
- A colon (`:`)
- A regular hyphen (`-`)
- Parentheses (`()`)
- Two sentences

### 4. No en-dashes as separators

En-dashes (`–`) used as separators (date ranges, number ranges) are banned. Use hyphens:
- "2018-2026" (not "2018–2026")
- "₹40-80k" (not "₹40–80k")

### 5. No em-dash / en-dash in code

The shipped HTML/CSS/JS has zero em-dashes or en-dashes. (They might appear in JavaScript string literals, but pre-flight sweeps rendered HTML only.)

---

## Soft rules (craft standard)

### 6. One voice per page

Don't mix technical mono, editorial prose, and marketing punch in the same composition unless the brand voice explicitly calls for it.

### 7. Concrete over abstract

| Don't | Do |
|---|---|
| "Premium experience" | "Same-day reports for routine tests." |
| "Expert team" | "Dr Priya (MBBS, MD Path), 12 years at Apollo" (real names + credentials) |
| "Personalized care" | "We WhatsApp you the report timing when you book." |

### 8. Local-first

If the business serves a specific city or area, say so. The prospect searches with a city attached.

- "Indore's most-booked salon for bridal makeup" (if true and verifiable)
- "Same-day reports for routine tests in Koramangala" (if real)
- "—" (if you can't verify the claim)

### 9. The CTA is concrete

| Don't | Do |
|---|---|
| "Get in touch" | "WhatsApp to book a haircut" |
| "Learn more" | "See our bridal packages" |
| "Start now" | "Book first class free" |
| "Reach out" | "Call 98765 43210" |
| "Contact us" | "WhatsApp 98765 43210" |
| "Submit" | "WhatsApp to confirm" |

One label per intent. No two CTAs with the same intent on one page.

### 10. Real photos only

No stock photos of people with arms in the air. No AI-generated portraits. No generic wellness imagery. Real photos of the real business, self-hosted, with `onerror` fallback to a branded monogram.

If the client has no usable photos, generate placeholder monogram tiles and tell them to swap later. Don't fill with stock photos that look generic.

### 11. Real reviews only

Reviews = Google review count + score + a "leave a review" CTA. No invented quotes. No "Sarah C. says: amazing service!" unless Sarah C. actually said it on the GBP.

If the GBP has 3 reviews, the site shows 3 reviews. If it has 0 reviews, the site shows "Be the first to leave a review" + a deep-link.

### 12. The hours are exactly what the GBP says

If the GBP says "Mon-Sat 9 AM - 7 PM, Sun closed", the site says exactly that. Not "Open daily". Not "9-7". Not "Mon-Sat" if the GBP says "Monday-Saturday".

The hours table highlights today (e.g. "Today: 9 AM - 7 PM" with a green dot).

### 13. The map is real

The map iframe points to the real address. If the GBP has coordinates, use those. If not, use the address string. OSM fallback at 1.5s in case the Google Maps iframe fails to load.

### 14. The phone numbers are real

Every WhatsApp CTA uses `wa.me/<digits>` with a real international-format number (no letters, no spaces, no `+` sign in the path). Every `tel:` CTA uses `tel:<digits>`. Both are verified by `link_probe.py`.

### 15. The photos have alt text

Every `<img>` has meaningful `alt`. Decorative images have `alt=""`.

---

## The copy self-audit

Before merging any page to main, re-read every visible string. Flag any string that:

- Is grammatically broken
- Has unclear referents
- Sounds like AI hallucination (cute-but-wrong wordplay, forced metaphors)
- Reads like an LLM trying to sound thoughtful

Rewrite every flagged string. If unsure, replace with a plain functional sentence.

---

## The Indore salon owner gut check

Before shipping any line of copy, ask:

> Would a salon owner in Indore scroll past this without re-reading?

If yes, rewrite. The hard floor on all customer-facing copy: **the prospect must understand every word without a dictionary.** Indian SMB customers don't think in "bespoke", "template", "premium", "Pro", "starter". They think "I need a real website" / "I need a website that looks like mine".

---

## Examples

### A good hero (salon)

```html
<h1>Good hair days start here.</h1>
<p>Walk-ins welcome. WhatsApp to skip the wait.</p>
<a class="btn btn--primary" href="https://wa.me/919876543210?text=Hi%2C%20I%27d%20like%20to%20book%20a%20haircut.%20When%27s%20the%20next%20slot%3F">WhatsApp to Book</a>
```

### A bad hero (forbidden)

```html
<h1>Elevate Your Beauty Experience.</h1>
<p>Discover the art of bespoke hair styling — crafted with care, delivered seamlessly.</p>
<a class="btn btn--primary" href="#">Learn More</a>
```

Why it's bad:
- "Elevate Your Beauty Experience" — AI tell
- "bespoke", "crafted with care", "delivered seamlessly" — three AI tells in one paragraph
- Em-dash
- "Learn More" — generic CTA that doesn't say what happens next
- `href="#"` — dead button

### A good services section (clinic)

```html
<h2>Tests we run.</h2>
<p>Same-day reports for routine tests. Home collection in Koramangala, Indiranagar, and surrounding areas.</p>
<ul>
  <li>CBC — 4-6 hours, no fasting, ₹350 — Confirm by WhatsApp</li>
  <li>Lipid profile — 4-6 hours, 8-hour fasting, ₹650 — Confirm by WhatsApp</li>
  <li>Thyroid (TSH) — same day, no fasting, ₹500 — Confirm by WhatsApp</li>
</ul>
<a class="btn btn--primary" href="https://wa.me/919876543210?text=Hi%2C%20I%27d%20like%20to%20book%20a%20test">WhatsApp to book a test</a>
```

### A bad services section (forbidden)

```html
<h2>Our Premium Diagnostic Services</h2>
<p>Experience world-class diagnostics — cutting-edge technology, seamless booking, India's leading lab.</p>
<ul>
  <li>Complete Blood Count — ₹350</li>
  <li>Lipid Profile — ₹650</li>
  <li>Thyroid Test — ₹500</li>
</ul>
<a class="btn btn--primary" href="tel:919876543210">Call us</a>
```

Why it's bad:
- "Premium Diagnostic Services" — empty marketing language
- "world-class", "cutting-edge", "seamless", "India's leading" — four AI tells
- Em-dash
- Prices with no "Confirm by WhatsApp" qualifier (these prices are real if the GBP says so, otherwise they should be marked)
- "Call us" — generic CTA
- Mixes call intent (phone) with booking intent (WhatsApp would be better)

---

## What this skill will never write

This list is appended to the pre-flight as a forbidden vocabulary check:

```
Elevate, Seamless, Unleash, Next-Gen, Next Generation, Revolutionary,
Crafted with care, Crafted with love, Game-changing, Cutting-edge,
Best-in-class, World-class, Industry-leading, Unparalleled, Unprecedented,
In today's fast-paced world, In today's world, In the modern era,
Quietly trusted by, Trusted by thousands, Loved by millions,
Transform your life, Transform your business, Unlock your potential,
We are passionate about, We are committed to, We pride ourselves on,
Holistic approach, Bespoke experience, Tailored solutions, Turnkey solution,
Synergy, Leverage, Synergize, Actionable insights, Move the needle,
Hit the ground running, At the end of the day, Going forward,
Circle back, Touch base, Deep dive, Low-hanging fruit, Paradigm shift,
Disrupt, Disruptive, Disruption, Pioneer, Pioneering, Trailblazer,
Revolutionize, Innovative solutions, Innovative approach,
Best practices, Optimal, Optimize, Optimization, Streamline,
Empower, Empowering, Empowerment, Enable, Enabler,
Robust, Scalable, Future-proof, Future-ready, Next-level,
Game-changer, Paradigm, Ecosystem, Platform, Solution,
— (em-dash anywhere visible)
– (en-dash as separator)
```

Any of these in shipped HTML = build fail.
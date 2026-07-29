# CRO Engines — the 7 industry-specific conversion patterns

The single biggest thing that earns the ₹24,999 price over the ₹9,999 tier is **the CRO engine** — the one interactive element on the home page that gives the visitor a reason to stay and pre-fills a high-intent WhatsApp message. Every engine ships with a `cro_test.py` that exercises every state-transition.

The engines are split across two versions:

- **v1 ships 4:** `test-picker`, `mood-picker`, `service-picker`, `quote-builder`
- **v1.5 ships 3:** `project-picker`, `stock-check`, `class-picker`

This document is the spec for each engine. The implementation lives in `templates/per-industry/<industry>/cro-<engine>.js`.

---

## 1. test-picker (clinic, diagnostic-centre, dental, physio, vet)

### What it does

The visitor picks a test. They see:
- The test name + category
- Fasting instructions (e.g. "8-hour fasting required")
- Sample type (blood / urine / saliva / swab)
- Report timing (e.g. "Same day, 6 hours")
- Home-collection toggle (when available)
- A WhatsApp CTA pre-filled with the test name in the message

### Why it earns the price

A clinic visitor has a specific question: *"can I get this test today?"* A 6-card services grid doesn't answer that. The picker answers it in 3 taps, then drives them to WhatsApp with the test name already in the message — the clinic just has to confirm pricing. Conversion rate doubles vs. a static grid.

### Data structure

```json
{
  "tests": [
    {
      "id": "cbc",
      "name": "Complete Blood Count (CBC)",
      "category": "Routine",
      "fasting": "No fasting",
      "sample": "Blood",
      "report_timing": "Same day, 4-6 hours",
      "home_collection": true,
      "whatsapp_message": "Hi, I'd like to book the CBC test. Can you confirm availability and price?"
    }
  ]
}
```

A clinic site ships with **at least 10 real tests**, real fields, real timings. "Confirm by WhatsApp" is an acceptable answer for price.

### State transitions (what `cro_test.py` verifies)

1. Initial render: all tests visible (or filterable by category)
2. Filter by category → only matching tests visible
3. Filter by "no fasting" → only non-fasting tests visible
4. Filter by "home collection" → only tests with home_collection=true visible
5. Pick a test → details panel populates
6. WhatsApp CTA opens wa.me with the test name pre-filled in the message
7. Home-collection toggle generates a different WhatsApp message
8. Reset filters → all tests visible again

### WhatsApp pre-fill format

```
Hi, I'd like to enquire about [TEST NAME].
Fasting: [fasting status]
Sample: [sample type]
Report timing: [report timing]
[Optional: Home collection requested]

Could you confirm availability and price?
```

### Anti-patterns

- Never invent prices. "Confirm by WhatsApp" is the honest answer.
- Never claim "fasting not required" for tests that require fasting.
- Never show a "Book Now" button that doesn't open WhatsApp.

---

## 2. mood-picker (restaurant, café, bakery)

### What it does

The visitor picks a mood. They get:
- A table-size selector (2 / 4 / 6 / 8+)
- A time-of-day selector (lunch / afternoon / dinner / late)
- An occasion selector (date / family / business / quick bite)
- A 3-slot recommendation based on the combination
- A WhatsApp CTA pre-filled with the combination

### Why it earns the price

A restaurant visitor with "date night" intent has a different question than one with "quick bite" intent. A static menu doesn't segment. The picker does, in 4 taps, and routes the right intent to the restaurant's WhatsApp — they know what the customer wants before they reply.

### Data structure

```json
{
  "moods": [
    {
      "id": "date_night",
      "label": "Date night",
      "description": "Quiet corner, slow service, candle-friendly.",
      "default_table": 2,
      "default_time": "dinner",
      "recommended_slots": ["Fri 7:30 PM", "Sat 7:30 PM", "Sat 8:00 PM"]
    },
    {
      "id": "family_lunch",
      "label": "Family lunch",
      "description": "Spacious table, kids menu, afternoon sun.",
      "default_table": 4,
      "default_time": "lunch",
      "recommended_slots": ["Sun 12:30 PM", "Sun 1:00 PM", "Sat 1:00 PM"]
    }
  ]
}
```

### State transitions

1. Initial render: 4 mood cards
2. Pick mood → table + time selectors appear
3. Adjust table size → table count updates
4. Adjust time of day → time slot list updates
5. Pick a slot → CTA activates
6. WhatsApp CTA opens wa.me with the combination pre-filled

### WhatsApp pre-fill format

```
Hi, I'd like to book a table for [OCCASION].
Table size: [N] people
Time: [TIME OF DAY] on [DAY]
Preferred slot: [SLOT]

Could you confirm availability?
```

### Anti-patterns

- Never invent "recommended slots" — only use real available times from the GBP hours.
- Never promise a table is available. Confirm by WhatsApp.
- Never claim "5-star ambiance" without a real source.

---

## 3. service-picker (salon, beauty, spa)

### What it does

The visitor picks a service. They get:
- A length selector (30 min / 45 min / 60 min / 90 min)
- A stylist preference (any / senior / specific name)
- A day preference (today / tomorrow / weekday / weekend)
- A 3-slot recommendation based on the combination
- A WhatsApp CTA pre-filled with the service + length + slot

### Why it earns the price

A salon visitor has two questions: *"can I get [service] in [length]?"* and *"is [stylist] free?"* A 6-card services grid doesn't answer either. The picker answers both in 4 taps.

### Data structure

```json
{
  "services": [
    {
      "id": "haircut_basic",
      "name": "Haircut — Basic",
      "length_minutes": 30,
      "category": "Hair",
      "stylists": ["any", "senior"]
    }
  ]
}
```

### State transitions

1. Initial render: services grid
2. Filter by category → only matching services
3. Filter by max-length → only services ≤ max length
4. Pick service → length + stylist + day selectors appear
5. Pick combination → 3 slots shown
6. Pick a slot → CTA activates
7. WhatsApp CTA opens wa.me pre-filled

### WhatsApp pre-fill format

```
Hi, I'd like to book [SERVICE NAME].
Length: [N] minutes
Stylist preference: [any/senior/name]
Day: [today/tomorrow/weekday/weekend]
Preferred slot: [SLOT]

Could you confirm availability?
```

---

## 4. project-picker (contractor, plumber, electrician, AC, mechanic, auto) — **v1.5**

### What it does

The visitor picks a project type. They get:
- A size selector (single room / multi-room / whole property)
- A photo upload (drag-drop or file picker)
- An "I need this urgently" toggle
- A WhatsApp CTA pre-filled with the project + photo attached

### State transitions

1. Initial render: project-type grid (6-8 types)
2. Pick type → size + photo + urgency appear
3. Upload photo(s) → preview thumbnails appear
4. Submit → WhatsApp opens with project + photo count + urgency in message
5. Server-side: photos get uploaded to a Formspree endpoint (₹1,499 setup, see `forge-positioning`)

### WhatsApp pre-fill format

```
Hi, I'd like a quote for [PROJECT TYPE].
Size: [single/multi/whole]
Photos attached: [N]
Urgency: [normal/urgent]

Could you confirm a free site visit?
```

---

## 5. stock-check (retail, boutique) — **v1.5**

### What it does

The visitor searches for a product. They get:
- A yes/no stock answer
- A "reserve for pickup" CTA
- A WhatsApp CTA pre-filled with the product name

### State transitions

1. Initial render: search input
2. Type product name → live results
3. Pick a product → stock status + size availability
4. Reserve → WhatsApp CTA with reserve details
5. Out-of-stock → "notify me when back" CTA

---

## 6. class-picker (fitness, gym, yoga, dance) — **v1.5**

### What it does

The visitor picks a class type. They get:
- The next 7-day schedule for that class
- A specific time slot
- A WhatsApp CTA pre-filled with the class + slot

### State transitions

1. Initial render: class type grid
2. Pick class type → 7-day schedule appears
3. Pick a slot → CTA activates
4. WhatsApp CTA opens wa.me pre-filled

### WhatsApp pre-fill format

```
Hi, I'd like to book the [CLASS TYPE] class.
Date: [DATE]
Time: [TIME]

Is this slot still available?
```

---

## 7. quote-builder (coach, tutor, consultant, B2B service, personal-brand)

### What it does

The visitor answers 4-5 questions about their situation. They get:
- A scope summary
- A "send this to me on WhatsApp" CTA
- An optional email-me-this-quote fallback

### Data structure

```json
{
  "questions": [
    {
      "id": "problem",
      "prompt": "What's the situation you're trying to address?",
      "type": "long_string",
      "required": true
    },
    {
      "id": "timeline",
      "prompt": "When do you need this addressed by?",
      "type": "enum",
      "options": ["This month", "Next 1-3 months", "Just exploring"]
    },
    {
      "id": "audience",
      "prompt": "Who else is involved in this decision?",
      "type": "string"
    },
    {
      "id": "budget",
      "prompt": "Have you set aside a budget for this?",
      "type": "enum",
      "options": ["Yes", "Not yet", "Prefer not to say"]
    }
  ]
}
```

### State transitions

1. Initial render: question 1 of N
2. Answer question → next question renders
3. After last question → scope summary appears
4. Submit → WhatsApp opens with the full scope as a pre-filled message
5. "Email me this instead" → opens mailto: with the scope in the body

### WhatsApp pre-fill format

```
Hi, I'd like to enquire about working together.

Situation: [ANSWER 1]
Timeline: [ANSWER 2]
Audience: [ANSWER 3]
Budget: [ANSWER 4]

Could we set up a discovery call?
```

---

## The universal anti-pattern (applies to all 7 engines)

1. **Never a "Book Now" button that doesn't open WhatsApp** (or tel:, or mailto:, or a real booking system).
2. **Never a filter that returns zero results without an empty state.**
3. **Never a state-transition that's invisible to the visitor** (silent state changes feel broken).
4. **Never a pre-fill message that's generic** ("Hi, I'd like more info" is broken — pre-fill with the picked item).
5. **Never a CRO engine that requires login.** Friction kills conversion.

Every engine ships with the same skeleton:

```html
<section class="cro-engine" data-engine="<engine-type>">
  <h2 class="cro-engine__heading">[Engine-specific heading]</h2>
  <p class="cro-engine__lede">[Engine-specific lede]</p>
  <div class="cro-engine__interactive">
    [Engine-specific UI — tests, moods, services, questions]
  </div>
  <a class="btn btn--primary cro-engine__cta" href="#" data-whatsapp-prefill>
    [Engine-specific CTA label]
  </a>
</section>
```

And:

```js
// cro-<engine>.js — vanilla, no deps
(function () {
  // State management
  // Filter / pick handlers
  // WhatsApp pre-fill composition
  // Open wa.me in new tab
})();
```

The pre-flight check `link_probe.py` verifies every CTA's href is a working wa.me / tel: / mailto: / external URL. The pre-flight check `cro_test.py` exercises every state-transition with a headless browser and captures a screenshot of each.
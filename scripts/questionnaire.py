#!/usr/bin/env python3
"""
forge-bespoke / scripts/questionnaire.py

Mode 3: Walk the 18-question conversational intake.

The agent runs this when the prospect has neither a GBP nor a PDF.
Each question is asked one at a time, conversationally. Skip rules
from assets/questionnaire.json prune questions based on prior answers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"


def load_questionnaire() -> dict:
    return json.loads((ASSETS / "questionnaire.json").read_text())


def should_skip(qid: str, answers: dict, qdef: dict) -> bool:
    for rule in qdef.get("skip_rules", []):
        if rule.get("skip") != qid:
            continue
        cond = rule.get("when", "")
        # Very small expression evaluator; supports simple `in` and `==`
        try:
            if cond == "":
                continue
            if " in [" in cond:
                var, opts = cond.split(" in ", 1)
                var = var.strip()
                opts = json.loads(opts)
                if answers.get(var) in opts:
                    return True
            elif "==" in cond:
                var, val = cond.split("==", 1)
                var = var.strip()
                val = val.strip().strip("'").strip('"')
                if answers.get(var) == val:
                    return True
        except Exception:
            pass
    return False


def walk(args, playbooks: dict, qdef: dict) -> dict:
    """Interactively walk the questionnaire. Returns a .client.json-shaped dict.

    The actual interaction is driven by the agent (one question per turn).
    This function provides the question flow + skip rules + the final
    normalized dict shape.
    """
    print("Questionnaire mode: ask each question in order, collect answers in this dict:", file=sys.stderr)
    print(json.dumps({}, indent=2), file=sys.stderr)
    print("Press Ctrl-C to abort.", file=sys.stderr)

    answers: dict = {}
    order = qdef.get("default_order", [])

    for qid in order:
        q = next((qq for qq in qdef["questions"] if qq["id"] == qid), None)
        if not q:
            continue
        if should_skip(qid, answers, qdef):
            continue

        # The agent asks this prompt. The user types the answer.
        # Real prompt would be: print(q["prompt"]); user_input = input()
        # For now, just emit the prompt and let the orchestrator handle.
        print(f"[Q] {q['prompt']}", file=sys.stderr)
        # placeholder: agent fills via stdin

    # Build the normalized client.json from the answers dict.
    return _answers_to_client(answers)


def _answers_to_client(answers: dict) -> dict:
    """Turn the questionnaire answers into a .client.json-shaped dict."""
    name = answers.get("q1_business_name", "Business")
    slug = __import__("re").sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    phone_raw = answers.get("q6_phone", "")
    whatsapp_raw = answers.get("q7_whatsapp", "")

    if phone_raw.startswith("+"):
        phone_intl = phone_raw.lstrip("+")
    else:
        phone_intl = "".join(c for c in phone_raw if c.isdigit() or c == "+").lstrip("+")
        if phone_intl and not phone_intl.startswith("91") and len(phone_intl) == 10:
            phone_intl = "91" + phone_intl

    if whatsapp_raw == "same_as_phone":
        whatsapp_intl = phone_intl
    elif whatsapp_raw:
        whatsapp_intl = "".join(c for c in whatsapp_raw if c.isdigit() or c == "+").lstrip("+")
        if whatsapp_intl and not whatsapp_intl.startswith("91") and len(whatsapp_intl) == 10:
            whatsapp_intl = "91" + whatsapp_intl
    else:
        whatsapp_intl = phone_intl

    return {
        "name": name,
        "slug": slug,
        "industry": None,
        "industry_candidates": [],
        "phone_raw": phone_intl,
        "phone_intl": phone_intl,
        "phone_display": "+" + phone_intl if phone_intl else "",
        "whatsapp_raw": whatsapp_intl,
        "whatsapp_intl": whatsapp_intl,
        "whatsapp_display": "+" + whatsapp_intl if whatsapp_intl else "",
        "whatsapp_url": f"https://wa.me/{whatsapp_intl}" if whatsapp_intl else "#",
        "email": answers.get("q8_email", ""),
        "address_full": answers.get("q5_city_area", ""),
        "address_short": answers.get("q5_city_area", ""),
        "hero_headline": answers.get("q2_what_you_do", name)[:80],
        "hero_subtext": answers.get("q3_target_customer", "")[:160],
        "tagline": answers.get("q2_what_you_do", "")[:80],
        "meta_description": answers.get("q2_what_you_do", f"{name} in {answers.get('q5_city_area', '')}."),
        "review_count": _parse_review_count(answers.get("q14a_review_count", "")),
        "rating": _parse_rating(answers.get("q14a_review_count", "")),
        "owner_name": answers.get("q1_business_name", name),
    }


def _parse_review_count(s: str) -> Optional[int]:
    if not s:
        return None
    m = __import__("re").search(r"(\d+)", s)
    return int(m.group(1)) if m else None


def _parse_rating(s: str) -> Optional[float]:
    if not s:
        return None
    m = __import__("re").search(r"(\d+\.?\d*)", s)
    return float(m.group(1)) if m else None


def main() -> None:
    # Standalone walk (rare; the agent usually orchestrates this).
    qdef = load_questionnaire()
    playbooks = json.loads((ASSETS / "industry-playbooks.json").read_text())

    class _Args:
        pass
    args = _Args()
    result = walk(args, playbooks, qdef)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
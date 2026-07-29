#!/usr/bin/env python3
"""
forge-bespoke / scripts/extract_from_gbp.py

Mode 2: Extract business signals from a Google Maps share URL.

Pipeline:
1. Open the GBP URL in camofox-browser (or fallback to curl + JSON-LD scraping)
2. Parse: name, phone, whatsapp, hours, photos, rating, review_count, address
3. Normalize to .client.json shape

This module is invoked by build.py --from-gbp. For the canonical full
audit (including category context, flags, calibration questions), use
forge-audit first. forge-bespoke uses the GBP for *website signals only*.

Real probe happens via camofox-browser when available; otherwise we
delegate the actual extraction to the orchestrator agent via --flags.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


def normalize_phone(raw: str) -> dict:
    """Return {display, raw_digits, intl_digits}."""
    if not raw:
        return {"display": "", "raw_digits": "", "intl_digits": ""}
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return {"display": raw, "raw_digits": "", "intl_digits": ""}
    if digits.startswith("91") and len(digits) == 12:
        intl = digits
    elif len(digits) == 10:
        intl = "91" + digits
    else:
        intl = digits
    display = "+" + intl
    return {"display": display, "raw_digits": intl, "intl_digits": intl}


def build_whatsapp_url(intl: str, message: str = "") -> str:
    msg = ("?text=" + __import__("urllib.parse").parse.quote(message)) if message else ""
    return f"https://wa.me/{intl}{msg}"


def extract(url: str, name: Optional[str] = None, whatsapp: Optional[str] = None, phone: Optional[str] = None) -> dict:
    """Run the GBP extraction. Returns a .client.json-shaped dict.

    Real implementation lives in the orchestrator agent (browser probes,
    JSON-LD parsing). This script provides the shape + helpers; the agent
    fills the data via --flags or via direct probes.
    """
    wa = normalize_phone(whatsapp or phone or "")
    ph = normalize_phone(phone or whatsapp or "")

    slug = re.sub(r"[^a-z0-9]+", "-", (name or "business").lower()).strip("-")

    return {
        "name": name or "Business",
        "slug": slug,
        "industry": None,  # orchestrator picks this from playbook
        "industry_candidates": [],
        "whatsapp_raw": wa["raw_digits"],
        "whatsapp_intl": wa["intl_digits"],
        "whatsapp_display": wa["display"],
        "whatsapp_url": build_whatsapp_url(wa["intl_digits"]),
        "phone_raw": ph["raw_digits"],
        "phone_intl": ph["intl_digits"],
        "phone_display": ph["display"],
        "email": "",
        "address_full": "",
        "address_short": "",
        "address_street": "",
        "address_city": "",
        "address_state": "",
        "address_postal": "",
        "directions_url": url,
        "google_maps_embed_url": url.replace("/place/", "/embed?pb=!1m18!1m12!1m3!1d"),
        "hours": {},
        "hours_jsonld": [],
        "hours_rows": "",
        "rating": None,
        "review_count": None,
        "rating_5_pct": None,
        "rating_jsonld": {},
        "google_reviews_url": url,
        "leave_review_url": url,
        "photos": [],
        "hero_photo": "/assets/hero.webp",
        "hero_photo_alt": "Storefront",
        "meta_description": "",
        "tagline": "",
        "hero_headline": name or "Business",
        "hero_subtext": "",
        "icp_persona": "the local practitioner",
        "primary_cta": "WhatsApp to Enquire",
        "owner_name": name or "Business",
        "owner_story_html": "<p>Story coming soon.</p>",
        "linkedin_url": "#",
        "cro_data": {},
    }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Extract signals from a GBP URL")
    parser.add_argument("--url", required=True)
    parser.add_argument("--name")
    parser.add_argument("--whatsapp")
    parser.add_argument("--phone")
    args = parser.parse_args()

    out = extract(args.url, name=args.name, whatsapp=args.whatsapp, phone=args.phone)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
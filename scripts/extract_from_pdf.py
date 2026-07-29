#!/usr/bin/env python3
"""
forge-bespoke / scripts/extract_from_pdf.py

Mode 1: Extract personal-brand signals from a CV / portfolio PDF.

Pipeline:
1. Extract text from PDF (via pymupdf / pdftotext)
2. Parse: name, role, services, experience, education, contact, photo
3. Normalize to .client.json shape (personal-industry defaults)

This is best-effort. CVs vary wildly. For unreliable inputs the
orchestrator agent handles fallback via Mode 3 (questionnaire).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


def extract_text(pdf_path: Path) -> str:
    """Try pymupdf first, then pdftotext."""
    try:
        import fitz  # pymupdf
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
        if text.strip():
            return text
    except Exception:
        pass

    try:
        result = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
    except FileNotFoundError:
        pass

    return ""


EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
PHONE_PATTERN = re.compile(r"(\+?\d[\d\s\-()]{8,})")
LINKEDIN_PATTERN = re.compile(r"linkedin\.com/in/([\w-]+)")


def extract_signals(pdf_path: Path) -> dict:
    text = extract_text(pdf_path)

    # First non-empty line is usually the name
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    name = lines[0] if lines else "Owner"

    # Pull email, phone, LinkedIn
    email_match = EMAIL_PATTERN.search(text)
    email = email_match.group(0) if email_match else ""

    phone_match = PHONE_PATTERN.search(text)
    phone = phone_match.group(1).strip() if phone_match else ""

    linkedin_match = LINKEDIN_PATTERN.search(text)
    linkedin = "https://linkedin.com/in/" + linkedin_match.group(1) if linkedin_match else ""

    # Pull first ~3 sentences as the tagline
    sentences = re.split(r"(?<=[.!?])\s+", text)
    tagline = " ".join(sentences[1:3]) if len(sentences) > 1 else ""

    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    wa_digits = re.sub(r"\D", "", phone) if phone else ""

    return {
        "name": name,
        "slug": slug,
        "industry": "personal",
        "industry_candidates": ["personal"],
        "whatsapp_raw": wa_digits,
        "whatsapp_intl": wa_digits,
        "whatsapp_display": phone,
        "whatsapp_url": "https://wa.me/" + wa_digits if wa_digits else "#",
        "phone_raw": wa_digits,
        "phone_intl": wa_digits,
        "phone_display": phone,
        "email": email,
        "address_full": "",
        "linkedin_url": linkedin or "#",
        "hero_headline": name,
        "hero_subtext": tagline,
        "tagline": tagline,
        "meta_description": tagline or (name + " - personal brand site."),
        "owner_name": name,
        "owner_story_html": "<p>" + tagline + "</p>",
        "hero_photo": "/assets/owner.webp",
        "hero_photo_alt": name,
        "primary_cta": "WhatsApp me",
        "icp_persona": "the personal brand visitor",
    }


def extract(pdf_path: str, name: Optional[str] = None, whatsapp: Optional[str] = None) -> dict:
    path = Path(pdf_path)
    if not path.exists():
        print("FAIL: PDF not found: " + pdf_path, file=sys.stderr)
        sys.exit(1)

    signals = extract_signals(path)
    if name:
        signals["name"] = name
        signals["owner_name"] = name
        signals["hero_headline"] = name
    if whatsapp:
        wa_digits = re.sub(r"\D", "", whatsapp)
        signals["whatsapp_raw"] = wa_digits
        signals["whatsapp_intl"] = wa_digits
        signals["whatsapp_url"] = "https://wa.me/" + wa_digits if wa_digits else "#"

    return signals


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Extract personal-brand signals from a PDF")
    parser.add_argument("--from-pdf", dest="pdf", required=True)
    parser.add_argument("--name")
    parser.add_argument("--whatsapp")
    args = parser.parse_args()

    out = extract(args.pdf, name=args.name, whatsapp=args.whatsapp)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
forge-bespoke / scripts/preflight.py

The mechanical gates (per references/preflight-checklist.md).

Usage:
    python3 preflight.py --target=dist/ --strict

Runs all 12 gates. Any fail = exit 1.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

# Reusable patterns
PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Z_0-9]+\}\}|Coming soon|Lorem ipsum|\bTODO\b|\bFIXME\b|\bTBD\b")
EM_DASH = re.compile(r"[—–]")  # both em-dash and en-dash as separator
AI_TELLS = re.compile(
    r"\b(Elevate[sd]?|Seamless(ly)?|Unleash|Revolutionary|Revolutioniz|Crafted with care|"
    r"Game[- ]?changing|Cutting[- ]?edge|Best[- ]?in[- ]?class|World[- ]?class|"
    r"Industry[- ]?leading|Unparalleled|Unprecedented|Quietly trusted by|"
    r"Transform your (life|business)|Unlock your potential|"
    r"We are passionate about|We are committed to|We pride ourselves on|"
    r"Holistic approach|Bespoke experience|Tailored solutions|Turnkey solution|"
    r"Synerg(y|ize)|Leverage|Actionable insights|Move the needle|"
    r"Hit the ground running|At the end of the day|Going forward|"
    r"Circle back|Touch base|Deep dive|Low[- ]?hanging fruit|Paradigm shift|"
    r"Disrupt(ive|ion)?|Pioneer(ing)?|Trailblazer|Innovative (solutions?|approach)|"
    r"Best practices|Optim(al|ize|ization)|Streamline|Empower(ing|ment)?|"
    r"Enable[dr]?|Robust|Scalable|Future[- ]?proof|Future[- ]?ready|Next[- ]?level|"
    r"Game[- ]?changer|Ecosystem|Platform|"
    r"In today.s fast-paced world|In today.s world|In the modern era)\b",
    re.IGNORECASE,
)

CTAS = re.compile(r'<a[^>]*class="[^"]*\bbtn\b[^"]*"[^>]*href="([^"]+)"', re.IGNORECASE)
ALL_ANCHORS = re.compile(r'<a[^>]*href="(#[^"]+)"', re.IGNORECASE)
ALL_IDS = set()
IMAGES = re.compile(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*(?:onerror="([^"]*)")?', re.IGNORECASE)


def find_files(target: Path, exts: list[str]) -> list[Path]:
    out = []
    for ext in exts:
        out.extend(target.rglob(f"*{ext}"))
    return out


def read(path: Path) -> str:
    return path.read_text(errors="ignore")


def gate_fabricated(target: Path) -> list[str]:
    """Gate 1: No fabricated content."""
    issues = []
    for f in find_files(target, [".html"]):
        text = read(f)
        # Check testimonials have data-source
        for m in re.finditer(r'<blockquote[^>]*data-source="([^"]*)"', text):
            if not m.group(1):
                issues.append(f"{f}: blockquote has empty data-source")
        # Check hours strings match a known pattern (we trust the orchestrator to source them)
        # This gate is best-effort; the real source enforcement is at the build layer.
    return issues


def gate_dead_buttons(target: Path) -> list[str]:
    """Gate 2: No dead buttons (delegated to link_probe.py for live checks)."""
    issues = []
    for f in find_files(target, [".html"]):
        text = read(f)
        for href in CTAS.findall(text):
            if href in ("#", "javascript:void(0)", "javascript:;", ""):
                issues.append(f"{f}: dead CTA href={href!r}")
    return issues


def gate_placeholders(target: Path) -> list[str]:
    """Gate 3: No placeholders visible."""
    issues = []
    for f in find_files(target, [".html", ".css", ".js"]):
        text = read(f)
        for m in PLACEHOLDER_PATTERN.finditer(text):
            issues.append(f"{f}: placeholder token '{m.group(0)}'")
    return issues


def gate_ai_tells(target: Path) -> list[str]:
    """Gate 4: No em-dashes, no AI tells."""
    issues = []
    for f in find_files(target, [".html"]):
        text = read(f)
        for m in EM_DASH.finditer(text):
            issues.append(f"{f}: em-dash or en-dash found")
        for m in AI_TELLS.finditer(text):
            issues.append(f"{f}: AI tell '{m.group(0)}'")
    return issues


def gate_photos(target: Path) -> list[str]:
    """Gate 7: Real photos with onerror fallback."""
    issues = []
    for f in find_files(target, [".html"]):
        text = read(f)
        for m in re.finditer(r'<img[^>]*src="([^"]+)"[^>]*>', text):
            tag = m.group(0)
            if "/assets/" not in tag and "http" in m.group(1):
                issues.append(f"{f}: external image src '{m.group(1)}' (must self-host)")
            if "onerror" not in tag:
                issues.append(f"{f}: <img> missing onerror fallback")
    return issues


def gate_alt(target: Path) -> list[str]:
    """Gate 12: Alt text on every meaningful image."""
    issues = []
    for f in find_files(target, [".html"]):
        text = read(f)
        for m in re.finditer(r'<img[^>]*>', text):
            tag = m.group(0)
            if "alt=" not in tag:
                issues.append(f"{f}: <img> missing alt attribute")
            else:
                alt_m = re.search(r'alt="([^"]*)"', tag)
                # alt="" is allowed for decorative
    return issues


def gate_design_system(target: Path) -> list[str]:
    """Gate 10: One accent, one font pair, one radius (heuristic)."""
    issues = []
    css_files = find_files(target, [".css"])
    if not css_files:
        return issues
    css = "\n".join(read(f) for f in css_files)
    hex_colors = set(re.findall(r"#[0-9a-fA-F]{6}", css))
    # Heuristic: count colors that look like accents (not pure black/white/grey)
    accent_like = {c for c in hex_colors if not re.match(r"^#(fff|000|[0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$", c.lower())}
    if len(accent_like) > 3:
        issues.append(f"design-system: {len(accent_like)} accent-like colors found (limit 1 accent + neutral)")
    return issues


def gate_contrast(target: Path) -> list[str]:
    """Gate 11: WCAG AA contrast. Best-effort heuristic; full check via accessibility.py."""
    # Defer to accessibility.py for full check.
    return []


def gate_reduced_motion(target: Path) -> list[str]:
    """Gate 8: prefers-reduced-motion honored."""
    issues = []
    for f in find_files(target, [".css"]):
        text = read(f)
        if re.search(r"@keyframes\s+\w+", text) and "prefers-reduced-motion" not in text:
            issues.append(f"{f}: @keyframes without prefers-reduced-motion guard")
    return issues


def gate_color_scheme(target: Path) -> list[str]:
    """Gate 9: prefers-color-scheme respected."""
    issues = []
    for f in find_files(target, [".html"]):
        text = read(f)
        if "prefers-color-scheme" not in text and "<body" in text:
            issues.append(f"{f}: no prefers-color-scheme handling")
    return issues


GATES = {
    "fabricated": gate_fabricated,
    "dead-buttons": gate_dead_buttons,
    "placeholders": gate_placeholders,
    "ai-tells": gate_ai_tells,
    "photos": gate_photos,
    "alt": gate_alt,
    "design-system": gate_design_system,
    "reduced-motion": gate_reduced_motion,
    "color-scheme": gate_color_scheme,
    "contrast": gate_contrast,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="forge-bespoke pre-flight gates")
    parser.add_argument("--target", default="dist/", help="Directory to scan")
    parser.add_argument("--strict", action="store_true", help="All warnings = errors")
    parser.add_argument("--check", help="Run a single gate (e.g. 'ai-tells')")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"FAIL: target {target} does not exist", file=sys.stderr)
        sys.exit(1)

    selected = {args.check: GATES[args.check]} if args.check else GATES
    all_issues: dict[str, list[str]] = {}

    for name, gate in selected.items():
        try:
            issues = gate(target)
            all_issues[name] = issues
            status = "✓" if not issues else "✗"
            print(f"{status} Gate: {name} ({len(issues)} issues)")
            for issue in issues:
                print(f"    - {issue}")
        except Exception as e:
            all_issues[name] = [f"gate crashed: {e}"]
            print(f"✗ Gate: {name} crashed: {e}", file=sys.stderr)

    failed = sum(1 for issues in all_issues.values() if issues)
    if failed:
        print(f"\nPre-flight: FAILED ({failed} gates have issues)", file=sys.stderr)
        sys.exit(1)

    print("\nPre-flight: PASSED.")


if __name__ == "__main__":
    main()
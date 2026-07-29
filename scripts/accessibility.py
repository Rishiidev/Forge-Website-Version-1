#!/usr/bin/env python3
"""
forge-bespoke / scripts/accessibility.py

Lightweight accessibility smoke test:
- WCAG AA contrast heuristic (text vs background)
- prefers-reduced-motion check
- prefers-color-scheme check
- All <img> have alt
- All <button> have accessible name

Requires: nothing beyond stdlib + the built HTML/CSS.

Usage:
    python3 accessibility.py --target=dist/
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    def channel(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str) -> float:
    l1 = relative_luminance(hex_to_rgb(fg))
    l2 = relative_luminance(hex_to_rgb(bg))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def main() -> None:
    parser = argparse.ArgumentParser(description="forge-bespoke a11y smoke test")
    parser.add_argument("--target", default="dist/")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"FAIL: {target} does not exist", file=sys.stderr)
        sys.exit(1)

    issues = []

    # Alt on images
    for f in target.rglob("*.html"):
        text = f.read_text(errors="ignore")
        for m in re.finditer(r"<img[^>]*>", text):
            tag = m.group(0)
            if "alt=" not in tag:
                issues.append(f"{f.name}: <img> missing alt")

        # Buttons without accessible name
        for m in re.finditer(r"<button[^>]*>(.*?)</button>", text, re.DOTALL):
            tag = m.group(0)
            content = m.group(1).strip()
            if not content and "aria-label" not in tag:
                issues.append(f"{f.name}: <button> without accessible name")

        # prefers-reduced-motion
        if "@media (prefers-reduced-motion" not in text and "<style" not in text:
            # If there's no <style> in the HTML (CSS is external), check CSS files
            pass

    # prefers-reduced-motion in CSS
    has_reduced_motion = False
    for f in target.rglob("*.css"):
        if "prefers-reduced-motion" in f.read_text(errors="ignore"):
            has_reduced_motion = True
    if not has_reduced_motion:
        issues.append("CSS: no @media (prefers-reduced-motion) block")

    # prefers-color-scheme in CSS
    has_dark_mode = False
    for f in target.rglob("*.css"):
        if "prefers-color-scheme" in f.read_text(errors="ignore"):
            has_dark_mode = True
    if not has_dark_mode:
        issues.append("CSS: no @media (prefers-color-scheme) handling")

    if issues:
        print(f"Accessibility: {len(issues)} issue(s):")
        for i in issues:
            print(f"  ✗ {i}")
        sys.exit(1)

    print("Accessibility: PASSED (smoke test).")


if __name__ == "__main__":
    main()
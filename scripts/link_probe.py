#!/usr/bin/env python3
"""
forge-bespoke / scripts/link_probe.py

Verifies every CTA in the built site resolves to a working target.

Acceptable targets:
- wa.me/<digits> with a real international number
- tel:<digits> with a real number
- mailto:<email>
- #<id> where <id> exists in the page
- https://... returning 2xx

Disallowed:
- href="#"
- href="javascript:void(0)"
- href=""
- href="javascript:;"

Usage:
    python3 link_probe.py --target=dist/
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

ALLOWED_SCHEMES = ("https:", "tel:", "mailto:", "wa.me", "#")
DEAD_HREFS = {"#", "javascript:void(0)", "javascript:;", ""}


def probe_url(url: str, timeout: float = 5.0) -> tuple[bool, str]:
    """HEAD request. Returns (ok, status_or_error)."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return (200 <= r.status < 400, str(r.status))
    except urllib.error.HTTPError as e:
        return (e.code < 400, str(e.code))
    except Exception as e:
        return (False, str(e))


def probe_tel(num: str) -> bool:
    return bool(re.fullmatch(r"\+?\d{8,15}", num))


def probe_mailto(addr: str) -> bool:
    return bool(re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", addr))


def probe_anchor(href_id: str, page_text: str) -> bool:
    return f'id="{href_id.lstrip("#")}"' in page_text


def check_cta(href: str, page_text: str) -> tuple[bool, str]:
    if href in DEAD_HREFS:
        return (False, f"dead href '{href}'")
    if href.startswith("#"):
        return (probe_anchor(href, page_text), f"anchor target")
    if href.startswith("tel:"):
        return (probe_tel(href[4:]), "tel")
    if href.startswith("mailto:"):
        return (probe_mailto(href[7:]), "mailto")
    if "wa.me/" in href or href.startswith("https://wa.me/"):
        # Don't actually open wa.me (it 404s without the right path). Just check format.
        m = re.search(r"wa\.me/(\d+)", href)
        if m and probe_tel(m.group(1)):
            return (True, "wa.me")
        return (False, "wa.me malformed")
    if href.startswith("http://") or href.startswith("https://"):
        ok, status = probe_url(href)
        return (ok, f"http {status}")
    return (False, f"unknown scheme '{href[:20]}'")


def main() -> None:
    parser = argparse.ArgumentParser(description="forge-bespoke link probe")
    parser.add_argument("--target", default="dist/")
    parser.add_argument("--skip-external", action="store_true",
                        help="Skip external HEAD probes (faster; anchors + tel + mailto + wa.me only)")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"FAIL: {target} does not exist", file=sys.stderr)
        sys.exit(1)

    failed = 0
    total = 0
    for f in target.rglob("*.html"):
        text = f.read_text(errors="ignore")
        for m in re.finditer(r'<a[^>]*class="[^"]*\bbtn\b[^"]*"[^>]*href="([^"]+)"', text):
            total += 1
            href = m.group(1)
            if args.skip_external and href.startswith("http"):
                continue
            ok, info = check_cta(href, text)
            if not ok:
                failed += 1
                print(f"✗ {f.name}: CTA href={href!r} → {info}", file=sys.stderr)
            else:
                print(f"✓ {f.name}: CTA href={href[:60]!r} → {info}")

    print(f"\n{total - failed}/{total} CTAs verified.")
    if failed:
        print(f"FAIL: {failed} dead CTAs", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
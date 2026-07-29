#!/usr/bin/env python3
"""
forge-bespoke / scripts/screenshots.py

Takes mobile (375x812) and desktop (1440x900) screenshots of every page.

Requires: playwright (pip install playwright && playwright install chromium)

Usage:
    python3 screenshots.py --url "https://<business>.vercel.app/" --pages index services reviews contact about --output dist/screenshots/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="forge-bespoke screenshots")
    parser.add_argument("--url", required=True)
    parser.add_argument("--pages", nargs="+", default=["index", "services", "reviews", "contact", "about"])
    parser.add_argument("--output", default="dist/screenshots/")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FAIL: playwright not installed", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Mobile (375x812)
        ctx_m = browser.new_context(
            viewport={"width": 375, "height": 812},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )
        page_m = ctx_m.new_page()

        for page_name in args.pages:
            url = args.url.rstrip("/") + "/" + ("" if page_name == "index" else page_name + ".html")
            page_m.goto(url, wait_until="networkidle")
            page_m.screenshot(path=str(output_dir / f"mobile-{page_name}.png"), full_page=True)
            print(f"  ✓ mobile {page_name}")
        ctx_m.close()

        # Desktop (1440x900)
        ctx_d = browser.new_context(viewport={"width": 1440, "height": 900})
        page_d = ctx_d.new_page()

        for page_name in args.pages:
            url = args.url.rstrip("/") + "/" + ("" if page_name == "index" else page_name + ".html")
            page_d.goto(url, wait_until="networkidle")
            page_d.screenshot(path=str(output_dir / f"desktop-{page_name}.png"), full_page=True)
            print(f"  ✓ desktop {page_name}")
        ctx_d.close()

        browser.close()

    print(f"\nScreenshots saved to {output_dir}/")


if __name__ == "__main__":
    main()
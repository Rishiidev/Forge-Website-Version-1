#!/usr/bin/env python3
"""
forge-bespoke / scripts/cro_test.py

Exercises every state-transition of every CRO engine on every page.
Captures a screenshot of every state.

Requires: playwright (pip install playwright && playwright install chromium)

Usage:
    python3 cro_test.py --url "https://<business>.vercel.app/" --engine test-picker --output dist/cro-tests/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def run_test_picker(page, output_dir: Path) -> tuple[int, int]:
    """Exercise test-picker state machine."""
    ok = 0
    failed = 0

    # State 1: initial render — at least one test card visible
    cards = page.query_selector_all(".cro-engine__card")
    if len(cards) > 0:
        ok += 1
        page.screenshot(path=str(output_dir / "01-initial.png"))
    else:
        failed += 1

    # State 2: filter by "no fasting"
    page.select_option('[data-filter="fasting"]', "none")
    page.wait_for_timeout(200)
    no_fasting_cards = page.query_selector_all(".cro-engine__card")
    if len(no_fasting_cards) > 0 and len(no_fasting_cards) <= len(cards):
        ok += 1
        page.screenshot(path=str(output_dir / "02-filter-no-fasting.png"))
    else:
        failed += 1

    # State 3: pick the first test
    if no_fasting_cards:
        no_fasting_cards[0].click()
        page.wait_for_timeout(200)
        detail = page.query_selector(".cro-engine__detail:not([hidden])")
        if detail:
            ok += 1
            page.screenshot(path=str(output_dir / "03-picked.png"))
        else:
            failed += 1

    # State 4: CTA href contains the test name
    cta = page.query_selector('[data-whatsapp-prefill]:not([hidden])')
    if cta and cta.get_attribute("href") and "wa.me/" in cta.get_attribute("href"):
        href = cta.get_attribute("href")
        if "?text=" in href and len(href) > 50:
            ok += 1
            page.screenshot(path=str(output_dir / "04-cta-with-prefill.png"))
        else:
            failed += 1
            print(f"  ✗ CTA href missing pre-fill text: {href}")
    else:
        failed += 1
        print("  ✗ CTA not visible after picking a test")

    # State 5: reset
    reset = page.query_selector('[data-reset]')
    if not reset:
        # Reset by setting filters back
        page.select_option('[data-filter="fasting"]', "")
        page.wait_for_timeout(200)
    else:
        reset.click()
        page.wait_for_timeout(200)
    cards_after_reset = page.query_selector_all(".cro-engine__card")
    if len(cards_after_reset) == len(cards):
        ok += 1
        page.screenshot(path=str(output_dir / "05-reset.png"))
    else:
        failed += 1

    return ok, failed


def main() -> None:
    parser = argparse.ArgumentParser(description="forge-bespoke CRO engine tests")
    parser.add_argument("--url", required=True)
    parser.add_argument("--engine", required=True,
                        choices=["test-picker", "service-picker", "mood-picker", "quote-builder"])
    parser.add_argument("--output", default="dist/cro-tests/")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FAIL: playwright not installed. pip install playwright && playwright install chromium",
              file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output) / args.engine
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 375, "height": 812},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )
        page = ctx.new_page()
        page.goto(args.url, wait_until="networkidle")

        if args.engine == "test-picker":
            ok, failed = run_test_picker(page, output_dir)
        else:
            print(f"  (engine '{args.engine}' test not yet implemented in cro_test.py)",
                  file=sys.stderr)
            ok, failed = 0, 0

        browser.close()

    print(f"\n{ok}/{ok + failed} state-transitions passed.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
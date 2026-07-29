#!/usr/bin/env python3
"""
forge-bespoke / scripts/lighthouse.py

Per-page Lighthouse runner. Fails if any page scores <95 on
performance, accessibility, best-practices, or SEO at mobile emulation.

Requires: lighthouse (npm i -g lighthouse) + chrome (headless).

Usage:
    python3 lighthouse.py --url "https://<business>.vercel.app/" --pages index services reviews contact about
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run_lighthouse(url: str, output_dir: Path, form_factor: str = "mobile") -> dict:
    """Run lighthouse and return parsed scores."""
    out_json = output_dir / "report.json"
    cmd = [
        "lighthouse", url,
        "--form-factor=" + form_factor,
        "--quiet",
        "--chrome-flags=--headless --no-sandbox",
        "--output=json",
        "--output-path=" + str(out_json),
    ]
    if not shutil.which("lighthouse"):
        print("FAIL: lighthouse CLI not installed. npm i -g lighthouse", file=sys.stderr)
        sys.exit(1)

    print(f"  running lighthouse on {url} ({form_factor})")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"FAIL: lighthouse error: {result.stderr[:300]}", file=sys.stderr)
        return {}

    if not out_json.exists():
        print(f"FAIL: lighthouse did not write {out_json}", file=sys.stderr)
        return {}

    report = json.loads(out_json.read_text())
    return {
        k: round(report["categories"][k]["score"] * 100)
        for k in ["performance", "accessibility", "best-practices", "seo"]
        if k in report.get("categories", {})
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="forge-bespoke lighthouse runner")
    parser.add_argument("--url", required=True, help="Base URL of the live site")
    parser.add_argument("--pages", nargs="+", default=["index", "services", "reviews", "contact", "about"])
    parser.add_argument("--form-factor", default="mobile")
    parser.add_argument("--output", default="dist/lighthouse/")
    parser.add_argument("--threshold", type=int, default=95, help="Minimum score per axis")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    failed = 0
    all_results = {}

    for page in args.pages:
        url = args.url.rstrip("/") + "/" + ("" if page == "index" else page + ".html")
        scores = run_lighthouse(url, output_dir / page, form_factor=args.form_factor)
        all_results[page] = scores

        if not scores:
            failed += 1
            continue

        for axis, score in scores.items():
            if score < args.threshold:
                failed += 1
                print(f"  ✗ {page} {axis}={score} (need ≥{args.threshold})")
            else:
                print(f"  ✓ {page} {axis}={score}")

        # Save per-page JSON
        (output_dir / page / "report.json").write_text(json.dumps(scores, indent=2))

    summary = output_dir / "summary.json"
    summary.write_text(json.dumps(all_results, indent=2))

    if failed:
        print(f"\nLighthouse: FAILED ({failed} axis/page misses)", file=sys.stderr)
        sys.exit(1)

    print(f"\nLighthouse: PASSED. All axes ≥{args.threshold} on all pages.")


if __name__ == "__main__":
    main()
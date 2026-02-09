#!/usr/bin/env python3
"""
Facebook Marketplace Ad Generator for Portable Storage Units.

Generates ads for every major city in the US and exports them
to CSV and/or JSON for bulk upload or manual posting.

Usage:
    python generate.py                          # Generate all ads, export both CSV + JSON
    python generate.py --format csv             # CSV only
    python generate.py --format json            # JSON only
    python generate.py --state "Kentucky"        # Only one state
    python generate.py --ads-per-city 3          # Multiple ad variations per city
    python generate.py --output-dir ./my_ads     # Custom output directory
    python generate.py --preview                 # Print a sample ad and stats, no export
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime

from us_cities import US_CITIES, get_all_cities, get_total_count
from ad_templates import generate_ad, generate_multiple_ads


def generate_all_ads(states=None, ads_per_city=1):
    """Generate ads for all cities, optionally filtered by state."""
    all_ads = []

    source = US_CITIES
    if states:
        source = {s: cities for s, cities in US_CITIES.items() if s in states}
        missing = set(states) - set(source.keys())
        if missing:
            print(f"Warning: States not found: {', '.join(missing)}")

    for state, cities in source.items():
        for city in cities:
            if ads_per_city == 1:
                all_ads.append(generate_ad(city, state))
            else:
                all_ads.extend(generate_multiple_ads(city, state, count=ads_per_city))

    return all_ads


def export_csv(ads, output_path):
    """Export ads to CSV format suitable for bulk operations."""
    fieldnames = [
        "title",
        "description",
        "city",
        "state",
        "location",
        "category",
        "condition",
        "tags",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for ad in ads:
            row = dict(ad)
            row["tags"] = "; ".join(row["tags"])
            writer.writerow(row)

    print(f"CSV exported: {output_path} ({len(ads)} ads)")


def export_json(ads, output_path):
    """Export ads to JSON format."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ads, f, indent=2, ensure_ascii=False)

    print(f"JSON exported: {output_path} ({len(ads)} ads)")


def export_per_state_csv(ads, output_dir):
    """Export one CSV file per state for organized posting."""
    by_state = {}
    for ad in ads:
        state = ad["state"]
        by_state.setdefault(state, []).append(ad)

    state_dir = os.path.join(output_dir, "by_state")
    os.makedirs(state_dir, exist_ok=True)

    for state, state_ads in sorted(by_state.items()):
        safe_name = state.lower().replace(" ", "_").replace(".", "")
        path = os.path.join(state_dir, f"{safe_name}.csv")
        export_csv(state_ads, path)

    print(f"\nPer-state CSVs exported to: {state_dir}/ ({len(by_state)} states)")


def preview_ads(ads):
    """Print a preview of the generated ads."""
    print("=" * 70)
    print("FACEBOOK MARKETPLACE AD GENERATOR - PREVIEW")
    print("Portable Storage Units - All US Cities")
    print("=" * 70)

    # Stats
    states = set(ad["state"] for ad in ads)
    print(f"\nTotal ads generated: {len(ads)}")
    print(f"States covered:      {len(states)}")
    print(f"Unique cities:       {len(set((ad['city'], ad['state']) for ad in ads))}")

    # Sample ad
    sample = ads[0]
    print(f"\n{'─' * 70}")
    print("SAMPLE AD:")
    print(f"{'─' * 70}")
    print(f"Title:     {sample['title']}")
    print(f"Location:  {sample['location']}")
    print(f"Category:  {sample['category']}")
    print(f"Condition: {sample['condition']}")
    print(f"Tags:      {', '.join(sample['tags'])}")
    print(f"\nDescription:\n{sample['description']}")
    print(f"{'─' * 70}")

    # State breakdown
    print("\nAds per state:")
    state_counts = {}
    for ad in ads:
        state_counts[ad["state"]] = state_counts.get(ad["state"], 0) + 1
    for state in sorted(state_counts):
        print(f"  {state}: {state_counts[state]} cities")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Facebook Marketplace ads for portable storage units across US cities."
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="both",
        help="Export format (default: both)",
    )
    parser.add_argument(
        "--state",
        action="append",
        dest="states",
        help="Filter to specific state(s). Can be repeated: --state Kentucky --state Ohio",
    )
    parser.add_argument(
        "--ads-per-city",
        type=int,
        default=1,
        help="Number of ad variations per city (default: 1)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (default: ./output/<timestamp>)",
    )
    parser.add_argument(
        "--per-state",
        action="store_true",
        help="Also export individual CSV files per state",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview ads and stats without exporting files",
    )

    args = parser.parse_args()

    # Generate
    print("Generating ads...")
    ads = generate_all_ads(states=args.states, ads_per_city=args.ads_per_city)

    if not ads:
        print("No ads generated. Check your --state filter.")
        sys.exit(1)

    # Preview mode
    if args.preview:
        preview_ads(ads)
        return

    # Set up output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "output", timestamp
        )

    os.makedirs(output_dir, exist_ok=True)

    # Export
    if args.format in ("csv", "both"):
        export_csv(ads, os.path.join(output_dir, "marketplace_ads.csv"))

    if args.format in ("json", "both"):
        export_json(ads, os.path.join(output_dir, "marketplace_ads.json"))

    if args.per_state:
        export_per_state_csv(ads, output_dir)

    # Summary
    preview_ads(ads)
    print(f"\nFiles saved to: {output_dir}/")


if __name__ == "__main__":
    main()

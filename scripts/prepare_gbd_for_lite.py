#!/usr/bin/env python3
"""Prepare an IHME/GHDx GBD-style CSV for a lightweight JupyterLite demo.

This script keeps only a small, browser-friendly subset and joins country
centroids from content/data/country_reference.csv. It does not download IHME
data; obtain data through the approved IHME/GHDx workflow and terms first.

Example:
    python scripts/prepare_gbd_for_lite.py         --input ~/Downloads/IHME_GBD_RESULTS.csv         --output-csv content/data/gbd_lite_country.csv         --output-geojson content/data/gbd_lite_country.geojson         --measure DALYs --metric Rate --age "Age-standardized" --sex Both         --years 2010 2015 2021         --causes "Malaria" "Tuberculosis" "Ischemic heart disease"
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def normalize_header(row: dict[str, str]) -> dict[str, str]:
    return {k.strip(): v for k, v in row.items()}


def keep(row: dict[str, str], args: argparse.Namespace) -> bool:
    checks = [
        ("measure_name", args.measure),
        ("metric_name", args.metric),
        ("age_name", args.age),
        ("sex_name", args.sex),
    ]
    for col, desired in checks:
        if desired and row.get(col, "").lower() != desired.lower():
            return False
    if args.years and str(row.get("year")) not in {str(y) for y in args.years}:
        return False
    if args.causes and row.get("cause_name") not in set(args.causes):
        return False
    return True


def load_country_ref(path: Path) -> dict[str, dict[str, str]]:
    refs = {}
    for row in read_csv(path):
        refs[row["iso3"]] = row
    return refs


def to_geojson(rows: Iterable[dict[str, str]]) -> dict:
    features = []
    for row in rows:
        lon = float(row.pop("longitude"))
        lat = float(row.pop("latitude"))
        props = dict(row)
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": props,
        })
    return {"type": "FeatureCollection", "features": features}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-csv", default=ROOT / "content/data/gbd_lite_country.csv", type=Path)
    parser.add_argument("--output-geojson", default=ROOT / "content/data/gbd_lite_country.geojson", type=Path)
    parser.add_argument("--country-ref", default=ROOT / "content/data/country_reference.csv", type=Path)
    parser.add_argument("--measure", default="DALYs")
    parser.add_argument("--metric", default="Rate")
    parser.add_argument("--age", default="Age-standardized")
    parser.add_argument("--sex", default="Both")
    parser.add_argument("--years", nargs="*", default=[])
    parser.add_argument("--causes", nargs="*", default=[])
    args = parser.parse_args()

    country_ref = load_country_ref(args.country_ref)
    rows = [normalize_header(r) for r in read_csv(args.input)]
    filtered = [r for r in rows if keep(r, args)]

    output_rows = []
    for row in filtered:
        iso3 = row.get("iso3") or row.get("ihme_loc_id") or row.get("location_code")
        if not iso3:
            # Try exact country-name match from reference.
            matches = [ref for ref in country_ref.values() if ref["location_name"] == row.get("location_name")]
            if matches:
                iso3 = matches[0]["iso3"]
        if not iso3 or iso3 not in country_ref:
            continue
        ref = country_ref[iso3]
        row["iso3"] = iso3
        row["longitude"] = ref["longitude"]
        row["latitude"] = ref["latitude"]
        output_rows.append(row)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    args.output_geojson.parent.mkdir(parents=True, exist_ok=True)

    if not output_rows:
        raise SystemExit("No rows remained after filtering and geocoding. Check filters and ISO3 fields.")

    fieldnames = sorted({k for r in output_rows for k in r.keys()})
    with args.output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    geojson_rows = [dict(r) for r in output_rows]
    with args.output_geojson.open("w", encoding="utf-8") as f:
        json.dump(to_geojson(geojson_rows), f, indent=2)

    print(f"Wrote {len(output_rows):,} rows to {args.output_csv}")
    print(f"Wrote GeoJSON to {args.output_geojson}")


if __name__ == "__main__":
    main()

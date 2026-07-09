"""Lightweight validation for the JupyterLite Global Health GIS repository.

This test intentionally avoids heavyweight geospatial dependencies so it can run
quickly in GitHub Actions and in constrained training environments.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
DATA = CONTENT / "data"
PROJECTS = CONTENT / "projects"


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")


def main() -> None:
    required = [
        ROOT / "README.md",
        ROOT / "environment.yml",
        ROOT / ".github" / "workflows" / "deploy.yml",
        DATA / "sample_gbd_like_burden.csv",
        DATA / "country_reference.csv",
        DATA / "gbd_country_points_2021.geojson",
        PROJECTS / "global_health_demo.geolibre.json",
    ]
    for path in required:
        require(path)

    with (DATA / "sample_gbd_like_burden.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("sample_gbd_like_burden.csv has no rows")
    for col in ["location_name", "iso3", "year", "measure_name", "metric_name", "age_name", "sex_name", "cause_name", "val"]:
        if col not in rows[0]:
            raise SystemExit(f"Missing sample data column: {col}")
    if any(r.get("source") != "SYNTHETIC_DEMO_NOT_IHME" for r in rows):
        raise SystemExit("Bundled demo data must remain clearly marked as synthetic")

    with (DATA / "gbd_country_points_2021.geojson").open(encoding="utf-8") as f:
        gj = json.load(f)
    if gj.get("type") != "FeatureCollection" or not gj.get("features"):
        raise SystemExit("Invalid or empty GeoJSON")

    with (PROJECTS / "global_health_demo.geolibre.json").open(encoding="utf-8") as f:
        project = json.load(f)
    for key in ["version", "name", "mapView", "layers", "metadata"]:
        if key not in project:
            raise SystemExit(f"GeoLibre project missing key: {key}")
    if not project["layers"]:
        raise SystemExit("GeoLibre project has no layers")

    # Validate notebooks as JSON documents.
    for nb_path in sorted(CONTENT.glob("*.ipynb")):
        with nb_path.open(encoding="utf-8") as f:
            nb = json.load(f)
        if nb.get("nbformat") != 4 or not nb.get("cells"):
            raise SystemExit(f"Invalid notebook: {nb_path}")

    print("Repository smoke test passed.")


if __name__ == "__main__":
    main()

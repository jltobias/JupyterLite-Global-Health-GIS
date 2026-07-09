# JupyterLite Global Health GIS

Browser-only geospatial demonstrations for global health programs using **JupyterLite**, **JupyterGIS**, and **GeoLibre**.

This repository is designed for GitHub Pages under the `jltobias` profile:

- JupyterLite site: `https://jltobias.github.io/jupyterlite-global-health-gis/lab/index.html`
- Notebook view: `https://jltobias.github.io/jupyterlite-global-health-gis/notebooks/index.html`
- GeoLibre project template: `content/projects/global_health_demo.geolibre.json`

> **Data warning:** the bundled burden values are synthetic and exist only so the notebooks and GIS project run immediately. They are not IHME estimates. Replace `content/data/sample_gbd_like_burden.csv` with an approved IHME/GHDx/GBD Results export before doing analysis or public communication.

## Why this repository

Global health training often struggles with accounts, server setup, Binder waits, JupyterHub operations, and desktop GIS installation. This project packages a lightweight demonstration as static files so learners can open a URL and run notebooks directly in the browser.

The demonstration workflow is:

1. Prepare a small GBD-style country table for browser use.
2. Convert it to GeoJSON.
3. Explore it in a JupyterLite notebook.
4. Display it with JupyterGIS.
5. Launch the same data as a GeoLibre Web project.
6. Publish everything through GitHub Pages.

## Contents

```text
content/
  00_welcome_global_health_gis.ipynb
  01_gbd_data_pipeline_template.ipynb
  02_jupytergis_global_health_points.ipynb
  03_geolibre_project_launcher.ipynb
  04_program_demo_storyboard.ipynb
  05_public_data_sources_and_ethics.ipynb
  data/
    sample_gbd_like_burden.csv           # synthetic, not IHME
    country_reference.csv                # lightweight ISO3 centroids
    gbd_country_points_2021.geojson      # generated demo GeoJSON
  projects/
    global_health_demo.geolibre.json     # GeoLibre project file
scripts/
  prepare_gbd_for_lite.py                # transform approved GBD-style CSVs
  smoke_test.py                          # lightweight repository validation
.github/workflows/
  deploy.yml                             # build and publish JupyterLite
  validate.yml                           # validate repo content
```

## Quick start on GitHub

1. Create a new public repository named `jupyterlite-global-health-gis` under `https://github.com/jltobias`.
2. Add these files to the repository and push to the `main` branch.
3. In **Settings → Pages**, choose **GitHub Actions** as the Pages source.
4. In **Settings → Actions → General**, allow the workflow enough permissions to deploy Pages.
5. Open the deployed JupyterLite site at `https://jltobias.github.io/jupyterlite-global-health-gis/lab/index.html`.

## Replacing the synthetic data with IHME/GHDx data

Download an approved GBD Results CSV from IHME/GHDx, keeping the extract small enough for browser use. A practical training subset is often:

- measure: `DALYs`, `Deaths`, `YLLs`, or `YLDs`
- metric: `Rate`
- age: `Age-standardized`
- sex: `Both`
- years: two to five selected years
- causes or risks: a small teaching set
- locations: countries or a program region

Then run:

```bash
python scripts/prepare_gbd_for_lite.py   --input /path/to/IHME_GBD_RESULTS.csv   --output-csv content/data/gbd_lite_country.csv   --output-geojson content/data/gbd_lite_country.geojson   --measure DALYs   --metric Rate   --age "Age-standardized"   --sex Both   --years 2010 2015 2021   --causes "Malaria" "Tuberculosis" "Ischemic heart disease"
```

Commit only data that you are allowed to redistribute. Add a visible citation and filter description to the notebooks, README, and GeoLibre project metadata.

## Suggested repository tagline

**One URL. Zero install. Browser-based global health geospatial analytics with JupyterLite, JupyterGIS, and GeoLibre.**

## Roadmap

- Add a real, approved non-commercial IHME/GHDx teaching subset with citation.
- Add country polygon boundaries or PMTiles for choropleth maps.
- Add a GeoLibre story map export for public health program briefings.
- Add Jupyter Book or JupyterLite-Sphinx lessons around each notebook.
- Add a small WHO GHO API example for data that can be fetched directly from public APIs.
- Add accessibility checks and low-bandwidth mode for country-team training.

## License

Code and documentation in this starter repository are MIT licensed. The bundled demonstration data are synthetic and may be replaced. Public health datasets brought into the repository remain under their original licenses and user agreements.

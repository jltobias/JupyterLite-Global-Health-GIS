# Data governance checklist

This repository is intended for public, aggregated, non-sensitive training data.

## Before committing a dataset

- Confirm that redistribution is allowed.
- Confirm that the dataset is public, aggregated, and suitable for GitHub Pages.
- Remove line lists, individual-level records, identifiers, exact patient coordinates, and private operational data.
- Keep files small enough for JupyterLite.
- Document filters, source, citation, license or user agreement, and download date.
- Include uncertainty intervals where relevant.

## Recommended pattern for IHME/GHDx

Do not commit full raw GBD downloads. Instead, commit a small approved teaching subset and record:

- GBD round and tool.
- Download date.
- Measure, metric, age, sex, years, causes/risks, and locations.
- Any transformation from the raw file.
- Required citation and terms.

## GitHub security hygiene

Never commit API keys, credentials, private URLs, internal server names, or tokens. If a secret is accidentally committed, rotate it and remove it from the Git history using your organization's standard security process.

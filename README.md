# Real Estate Pricing Agent (Demo)

A small property price estimator agent: given a home's city, size, room
counts, age, and lot size, it returns an estimated price, a price range,
and the nearest comparable listings from a bundled dataset.

> **Disclaimer:** This is a demo/simulation built on a small synthetic
> dataset (240 generated listings). It is **not** a real appraisal tool
> and should never be used for actual pricing, lending, or investment
> decisions.

## Why this exists

This project is part of a daily build series exploring trending AI
application patterns -- this one focuses on a small, self-contained
"prediction agent" pattern: fit a lightweight model on structured data at
startup, expose it as both a CLI and an HTTP API, and return not just a
point estimate but supporting evidence (comparable listings + an error
range), the way an agent tool call should return something a caller can
actually reason about.

## What's under the hood

- `app/data/listings.csv` -- 240 synthetic property listings (city, sqft,
  bedrooms, bathrooms, year built, lot size, price). Generated
  procedurally with a fixed random seed, not real listing data.
- `app/model.py` -- a linear regression estimator fit with `numpy`
  least-squares (no scikit-learn dependency) over sqft, bedrooms,
  bathrooms, lot size, home age, and a one-hot city term. Reports RMSE
  as an error band and surfaces the 3 nearest-by-size comparables in the
  same city.
- `app/main.py` -- a FastAPI service exposing `/estimate`, `/cities`, and
  `/health`.
- `app/cli.py` -- a command-line entry point for a single estimate
  without running the API.

## Setup

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Then:

```bash
curl -X POST http://127.0.0.1:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Rivertown",
    "sqft": 1800,
    "bedrooms": 3,
    "bathrooms": 2,
    "year_built": 2005,
    "lot_size": 5000
  }'
```

## Run via CLI

```bash
python -m app.cli --city Rivertown --sqft 1800 --bedrooms 3 --bathrooms 2 \
  --year-built 2005 --lot-size 5000
```

## Run tests

```bash
pytest -q
```

9 tests cover data loading, model fitting/prediction sanity (positive
prices, larger homes pricing higher, unknown-city rejection), and the API
endpoints.

## Known limitations

- Trained on 240 synthetic rows -- not enough data, and not real data,
  for anything beyond a demo.
- Linear regression only; no interaction terms, no outlier handling.
- City list is fixed to the 5 synthetic cities baked into the dataset.

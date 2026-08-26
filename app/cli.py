"""Command-line entry point: run a single price estimate without the API.

Example:
    python -m app.cli --city Rivertown --sqft 1800 --bedrooms 3 --bathrooms 2 \
        --year-built 2005 --lot-size 5000
"""
from __future__ import annotations

import argparse
import json

from app.model import get_estimator


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate a property's price (demo, synthetic data).")
    parser.add_argument("--city", required=True)
    parser.add_argument("--sqft", type=int, required=True)
    parser.add_argument("--bedrooms", type=int, required=True)
    parser.add_argument("--bathrooms", type=int, required=True)
    parser.add_argument("--year-built", type=int, required=True)
    parser.add_argument("--lot-size", type=int, required=True)
    args = parser.parse_args()

    estimator = get_estimator()
    try:
        result = estimator.estimate(
            sqft=args.sqft,
            bedrooms=args.bedrooms,
            bathrooms=args.bathrooms,
            year_built=args.year_built,
            lot_size=args.lot_size,
            city=args.city,
        )
    except ValueError as e:
        parser.error(str(e))
        return

    print(json.dumps(result, indent=2))
    print("\nDemo estimate only, from a small synthetic dataset. Not a real appraisal or financial advice.")


if __name__ == "__main__":
    main()

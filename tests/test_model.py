import math

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.model import PriceEstimator, load_listings


def test_load_listings_nonempty():
    listings = load_listings()
    assert len(listings) > 100
    assert all(l.price > 0 for l in listings)


def test_estimator_fits_and_predicts_positive():
    estimator = PriceEstimator()
    result = estimator.estimate(
        sqft=1800, bedrooms=3, bathrooms=2, year_built=2005, lot_size=5000,
        city=estimator.cities[0],
    )
    assert result["estimated_price"] > 0
    assert result["price_range_low"] <= result["estimated_price"] <= result["price_range_high"]
    assert len(result["comparables"]) == 3


def test_estimator_rejects_unknown_city():
    estimator = PriceEstimator()
    with pytest.raises(ValueError):
        estimator.estimate(
            sqft=1500, bedrooms=3, bathrooms=2, year_built=2000, lot_size=4000,
            city="Nowhereville",
        )


def test_larger_home_generally_estimates_higher():
    estimator = PriceEstimator()
    city = estimator.cities[0]
    small = estimator.estimate(sqft=900, bedrooms=2, bathrooms=1, year_built=2005,
                                lot_size=3000, city=city)
    large = estimator.estimate(sqft=3200, bedrooms=4, bathrooms=3, year_built=2005,
                                lot_size=3000, city=city)
    assert large["estimated_price"] > small["estimated_price"]


def test_model_rmse_is_finite_and_reasonable():
    estimator = PriceEstimator()
    assert math.isfinite(estimator.rmse)
    assert estimator.rmse >= 0


client = TestClient(app)


def test_api_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_api_cities():
    resp = client.get("/cities")
    assert resp.status_code == 200
    assert len(resp.json()["cities"]) > 0


def test_api_estimate_success():
    resp = client.post("/estimate", json={
        "city": "Rivertown",
        "sqft": 1800,
        "bedrooms": 3,
        "bathrooms": 2,
        "year_built": 2005,
        "lot_size": 5000,
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["estimated_price"] > 0
    assert "disclaimer" in body


def test_api_estimate_unknown_city_400():
    resp = client.post("/estimate", json={
        "city": "Nowhereville",
        "sqft": 1800,
        "bedrooms": 3,
        "bathrooms": 2,
        "year_built": 2005,
        "lot_size": 5000,
    })
    assert resp.status_code == 400

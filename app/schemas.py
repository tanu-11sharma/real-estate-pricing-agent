from pydantic import BaseModel, Field


class EstimateRequest(BaseModel):
    city: str = Field(..., description="City name, e.g. 'Springfield'")
    sqft: int = Field(..., gt=100, le=20000)
    bedrooms: int = Field(..., ge=0, le=15)
    bathrooms: int = Field(..., ge=0, le=15)
    year_built: int = Field(..., ge=1800, le=2026)
    lot_size: int = Field(..., ge=0, le=200000, description="Lot size in sqft")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Rivertown",
                "sqft": 1800,
                "bedrooms": 3,
                "bathrooms": 2,
                "year_built": 2005,
                "lot_size": 5000,
            }
        }


class Comparable(BaseModel):
    id: int
    city: str
    sqft: int
    bedrooms: int
    bathrooms: int
    price: int


class EstimateResponse(BaseModel):
    estimated_price: float
    price_range_low: float
    price_range_high: float
    model_rmse: float
    comparables: list[Comparable]
    disclaimer: str = (
        "Demo estimate only, generated from a small synthetic dataset. "
        "Not a real appraisal and not financial advice."
    )

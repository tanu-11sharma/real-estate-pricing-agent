from fastapi import FastAPI, HTTPException

from app.model import get_estimator
from app.schemas import EstimateRequest, EstimateResponse

app = FastAPI(
    title="Real Estate Pricing Agent (Demo)",
    description=(
        "A small property price estimator agent trained on a bundled "
        "synthetic listings dataset. Demo/simulation only -- not a real "
        "appraisal tool and not financial advice."
    ),
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/cities")
def cities():
    estimator = get_estimator()
    return {"cities": estimator.cities}


@app.post("/estimate", response_model=EstimateResponse)
def estimate(req: EstimateRequest):
    estimator = get_estimator()
    try:
        result = estimator.estimate(
            sqft=req.sqft,
            bedrooms=req.bedrooms,
            bathrooms=req.bathrooms,
            year_built=req.year_built,
            lot_size=req.lot_size,
            city=req.city,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result

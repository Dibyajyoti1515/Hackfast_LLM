from fastapi import APIRouter, Body
from app.Function.profile_intelligence import extract_profile_features
from app.Function.run_gift_pipeline import run_gift_pipeline
import asyncio
router = APIRouter(prefix="/profile", tags=["Profile Intelligence"])

@router.post("/intelligence")
async def profile_intelligence(payload: dict = Body(...)):

    result = extract_profile_features(payload)
    results = await run_gift_pipeline(result)

    return {
        "result":results,
    }
from fastapi import APIRouter, Body
from app.Function.profile_intelligence import extract_profile_features
from app.Function.run_gift_pipeline_professional_intelligence import run_gift_pipeline
import asyncio
router = APIRouter(prefix="/professional", tags=["Profile Intelligence"])

@router.post("/intelligence")
async def profile_intelligence(payload: dict = Body(...)):

    result = extract_profile_features(payload)
    results = await run_gift_pipeline(result)

    return {
        "result":results,
    }

#describe_professional_intelligence
from fastapi import APIRouter, Body
from app.Function.extract_enrich_profile_features import extract_profile_features
from app.Function.run_enrich_gift_pipline import run_gift_pipeline

router = APIRouter(prefix="/enrich", tags=["Enrich Intelligence"])

@router.post("/intelligence")
async def enrich_intelligence(payload: dict = Body(...)):
    data = payload.get("data")
    user_hints = payload.get("userHints")

    if not data:
        return {
            "success": False,
            "message": "Missing 'data' in request payload"
        }

    profile_features = extract_profile_features(data)
    combined_payload = {
        "data": profile_features,
        "userHints": user_hints
    }

    print(combined_payload)
    results = await run_gift_pipeline(combined_payload)

    return {
        "success": True,
        "result": results
    }

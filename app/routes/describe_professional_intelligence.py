from fastapi import APIRouter, Body
# from app.Function.profile_intelligence import extract_profile_features
from app.Function.run_gift_pipeline_professional_intelligence import run_gift_pipeline
import asyncio
router = APIRouter(prefix="/describe", tags=["Profile Intelligence"])

def extract_profile_features(payload: dict):
    """
    Supports BOTH:
    1. Instagram structured payloads
    2. Text-based payloads: { requestId, prompt }

    Always returns:
    {
        "mode": "text" | "instagram",
        "text": "<normalized text>"
    }
    """

    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict")

    # ✅ TEXT MODE (Describe / Prompt Mode)
    if "prompt" in payload and isinstance(payload["prompt"], str):
        text = payload["prompt"].strip()

        if not text:
            raise ValueError("Prompt text is empty")

        print("📝 extract_profile_features → TEXT MODE")

        return {
            "mode": "text",
            "text": text
        }

    # ✅ LEGACY MODE (Instagram Payload)
    print("📸 extract_profile_features → INSTAGRAM MODE")

    user = payload.get("user") or {}
    captions = payload.get("captions") or payload.get("data") or []

    biography = user.get("biography", "")
    full_name = user.get("full_name", "")
    category = user.get("category", "")
    username = user.get("username", "")

    caption_text = " ".join(
        c for c in captions if isinstance(c, str)
    )

    combined_text = " ".join([
        username,
        full_name,
        category,
        biography,
        caption_text
    ]).strip()

    if not combined_text:
        raise ValueError("No usable text found in payload")

    return {
        "mode": "instagram",
        "text": combined_text
    }


@router.post("/intelligence")
async def profile_intelligence(payload: dict = Body(...)):

    result = extract_profile_features(payload)
    results = await run_gift_pipeline(result)

    return {
        "result":results,
    }
#run_gift_pipeline_describe_intelligence

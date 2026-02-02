from google.adk.runners import Runner
from google.adk.apps import App
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uuid
import json

from app.LLMAgents.describe_gift_recommendation_agent import gift_recommendation_pipeline

APP_NAME = "Gift Recommendation"


def normalize_llm_json(raw):
    if raw is None:
        return None

    if isinstance(raw, dict):
        return raw

    if not isinstance(raw, str):
        return raw

    text = raw.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]

    try:
        return json.loads(text)
    except Exception:
        print("❌ Failed to normalize JSON from LLM")
        print("RAW:", raw)
        print("CLEANED:", text)
        return None


def extract_agent_outputs(events: list):
    product_response = None
    profile_response = None

    for event in events:
        actions = getattr(event, "actions", None)
        if not actions:
            continue

        state_delta = getattr(actions, "state_delta", None)
        if not state_delta:
            continue

        if "product_extraction_response" in state_delta:
            raw = state_delta["product_extraction_response"]
            product_response = normalize_llm_json(raw)

        if "profile_analyzer_response" in state_delta:
            profile_response = state_delta["profile_analyzer_response"]

    return {
        "product_extraction_response": product_response,
        "profile_analyzer_response": profile_response
    }


# 🌱 Services
session_service = InMemorySessionService()

support_app = App(
    name=APP_NAME,
    root_agent=gift_recommendation_pipeline,
)

runner = Runner(
    app=support_app,
    session_service=session_service
)


# 🧠 TEXT PIPELINE ENTRYPOINT
# 🧠 TEXT PIPELINE ENTRYPOINT
async def run_gift_pipeline(payload: dict):
    print("📦 Incoming payload:", payload)

    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict")

    # ✅ CASE 1: New text-based pipeline
    if "text" in payload and isinstance(payload["text"], str):
        prompt_text = payload["text"].strip()

        if not prompt_text:
            raise ValueError("payload.text is empty")

        print("📝 Using direct text prompt")

    # ✅ CASE 2: Legacy structured payload (fallback)
    else:
        print("🧱 Using structured payload fallback")

        parts = []
        for key, value in payload.items():
            clean_value = str(value).replace("\n", " ").strip()
            if clean_value:
                parts.append(f"{key}: {clean_value}")

        prompt_text = ". ".join(parts)

        if not prompt_text.strip():
            raise ValueError("Failed to build prompt text from payload")

    # 🧬 Generate identity
    session_id = str(uuid.uuid4())
    user_id = session_id   # keep unique identity internally

    result_events = []

    content = types.Content(
        role="user",
        parts=[types.Part(text=prompt_text)]
    )

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    async for event in runner.run_async(
        user_id=user_id,
        new_message=content,
        session_id=session.id,
    ):
        print("📡 EVENT:", event)
        result_events.append(event)

    extracted = extract_agent_outputs(result_events)

    print("✅ Extracted:", extracted)

    return {
        "result": extracted,
        "status": "ok"
    }

from google.adk.runners import Runner
from google.adk.apps import App
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uuid
import json

from app.LLMAgents.romantic_gift_recommendation_agent import gift_recommendation_pipeline

APP_NAME = "Gift Recommendation"
USER_ID = "Dgjjg"
session_name = "hello"

def payload_to_prompt_string(payload: dict) -> str:
    parts = []
    for key, value in payload.items():
        clean_value = str(value).replace("\n", " ").strip()
        parts.append(f"[{key}: {clean_value}]")
    return ", ".join(parts)

def normalize_llm_json(raw):
    if raw is None:
        return None

    # ✅ Already parsed dict
    if isinstance(raw, dict):
        return raw

    if not isinstance(raw, str):
        return raw

    text = raw.strip()

    # ✅ Try direct JSON first
    try:
        return json.loads(text)
    except Exception:
        pass

    # ✅ Remove markdown fences
    text = text.replace("```json", "").replace("```", "").strip()

    # ✅ Extract JSON between first { and last }
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]

    try:
        return json.loads(text)
    except Exception as e:
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
            raw = state_delta["profile_analyzer_response"]
            try:
                profile_response = json.loads(raw)
            except Exception:
                profile_response = raw

    return {
        "product_extraction_response": product_response,
        "profile_analyzer_response": profile_response
    }

session_service = InMemorySessionService()

support_app = App(
    name=APP_NAME,
    root_agent=gift_recommendation_pipeline,
)

runner = Runner(
    app=support_app,
    session_service=session_service
)


async def run_gift_pipeline(payload: dict):

    conversation_text = payload_to_prompt_string(payload)
    session_id = str(uuid.uuid4())
    result = []

    content = types.Content(
        role="user",
        parts=[types.Part(text=conversation_text)]
    )

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        new_message=content,
        session_id=session.id,
    ):
        print(event)
        result.append(event)

    extracted = extract_agent_outputs(result)

    print(extracted)

    return {
        "result": extracted,
        "status": "ok"
    }

from google.adk.runners import Runner
from google.adk.apps import App
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uuid
import json



from app.LLMAgents.gift_recommendation_agent import gift_recommendation_pipeline

APP_NAME = "Gift Recommendation"
USER_ID = "Dgjjg"
session_name = "hello"

def payload_to_prompt_string(payload: dict) -> str:
    parts = []
    for key, value in payload.items():
        clean_value = str(value).replace("\n", " ").strip()
        parts.append(f"[{key}: {clean_value}]")
    return ", ".join(parts)

import json

def extract_agent_outputs(events: list):
    product_response = None
    profile_response = None

    for event in events:
        actions = getattr(event, "actions", None)
        if not actions:
            continue

        # ✅ Correct attribute name
        state_delta = getattr(actions, "state_delta", None)
        if not state_delta:
            continue

        # state_delta is a dict ✔️
        if "product_extraction_response" in state_delta:
            raw = state_delta["product_extraction_response"]
            try:
                product_response = json.loads(raw)
            except Exception:
                product_response = raw

        if "profile_analyzer_response" in state_delta:
            profile_response = state_delta["profile_analyzer_response"]

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

    return {
        "result": extracted,
        "status": "djjdjdjjdjdjddjj",
    }
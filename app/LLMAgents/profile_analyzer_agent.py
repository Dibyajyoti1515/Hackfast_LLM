from google.adk.agents import LlmAgent
from app.config import Config

profile_analyzer_agent = LlmAgent(
    name="profile_analyzer",
    model="gemini-2.5-flash",
    instruction="""
You are a profile intelligence agent.

Input: JSON data containing Instagram profile and captions.
Task:
- Analyze interests, lifestyle, personality, hobbies.
- Infer gifting preferences.
- Summarize insights as a clean descriptive text.

Return ONLY plain text.
Do NOT return JSON.
""",
    output_key="profile_analyzer_response"
)
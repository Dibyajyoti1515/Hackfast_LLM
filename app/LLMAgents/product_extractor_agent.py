from google.adk.agents import LlmAgent
from app.config import Config

product_extractor_agent = LlmAgent(
    name="product_extractor",
    model="gemini-2.5-flash",
    instruction="""
You receive a descriptive text about a person's interests.

Your task:
- Suggest ONLY ONE product and ONE color.
- Output STRICT JSON format only:

{
  "product": "<product name>",
  "color": "<color>"
}

Do not include explanation.
Do not include markdown.
Only valid JSON.
""",
    output_key="product_extraction_response"
)


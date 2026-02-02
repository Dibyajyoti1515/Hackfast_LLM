from google.adk.agents import ParallelAgent

from app.LLMAgents.enrich_profile_analyzer_agent import enrich_profile_analyzer_agent
from app.LLMAgents.enrich_product_extractor_agent import enrich_product_extractor_agent

enrich_gift_recommendation_pipeline = ParallelAgent(
    name="gift_pipeline",
    sub_agents=[
        enrich_profile_analyzer_agent,
        enrich_product_extractor_agent,
    ]
)
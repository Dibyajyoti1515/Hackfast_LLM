from google.adk.agents import ParallelAgent

from app.LLMAgents.describe_profile_analyzer_agent import profile_analyzer_agent
from app.LLMAgents.describe_product_extractor_agent import product_extractor_agent

gift_recommendation_pipeline = ParallelAgent(
    name="professional_gift_pipeline",
    sub_agents=[
        profile_analyzer_agent,
        product_extractor_agent,
    ]
)


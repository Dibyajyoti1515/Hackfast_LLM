from google.adk.agents import ParallelAgent

from app.LLMAgents.profile_analyzer_agent import profile_analyzer_agent
from app.LLMAgents.product_extractor_agent import product_extractor_agent

gift_recommendation_pipeline = ParallelAgent(
    name="gift_pipeline",
    sub_agents=[
        profile_analyzer_agent,
        product_extractor_agent
    ]
)
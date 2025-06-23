"""
Sequential Agent with a Minimal Callback

This example demonstrates a email autoresponder with a minimal 
before_agent_callback that only initializes state once at the begining.

"""

from google.adk.agents import SequentialAgent

from .subagents.response import response_generator_agent

root_agent = SequentialAgent(
    name="EmailAutoresponder",
    sub_agents=[response_generator_agent],
    description="An email autoresponder that summarizes, creates response and sends it back to the uesr."
)
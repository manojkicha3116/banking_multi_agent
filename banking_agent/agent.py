"""Banking Coordinator Agent

Root agent for a simple ADK multi-agent banking assistant.
It doesn't do any banking work itself -- it uses its instructions and the
`description` of each sub-agent to decide which specialist should handle
the user's request (LLM-driven delegation / ADK AutoFlow).

Run with:
    adk web banking_agent      # web UI
    adk run banking_agent      # interactive CLI
or import `root_agent` and drive it programmatically (see main.py).
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from banking_agent.sub_agents.balance_agent import balance_agent
from banking_agent.sub_agents.transactions_agent import transactions_agent
from banking_agent.sub_agents.fraud_agent import fraud_agent
from banking_agent.config.model_config import ModelManager

root_agent = LlmAgent(
    name="banking_coordinator",
    #model="gemini-2.5-flash",
    model=ModelManager.get_model(),
    description="Top-level banking assistant that routes customer requests to the right specialist.",
    instruction=(
        "You are the front door of a bank's virtual assistant. Greet the user "
        "briefly and figure out what they need, then delegate:\n"
        "- Balance or account-listing questions -> balance_agent\n"
        "- Transaction history / statement / specific transaction lookups -> transactions_agent\n"
        "- Reporting fraud, disputing a charge, or blocking a card -> fraud_agent\n"
        "Do not attempt to answer banking-specific questions yourself; always "
        "delegate to the right specialist sub-agent. If the request spans "
        "multiple areas, handle them one at a time. If the request is "
        "unrelated to banking, politely say you can only help with banking."
    ),
    sub_agents=[balance_agent, transactions_agent, fraud_agent],
)

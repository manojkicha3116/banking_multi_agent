"""Balance Agent

Handles queries about account balances and account summaries.
In a real deployment, get_account_balance would call a core-banking
API instead of returning mock data.
"""

from google.adk.agents import LlmAgent
from banking_agent.config.model_config import ModelManager

# --- Mock "core banking" data store -----------------------------------
_MOCK_ACCOUNTS = {
    "ACC1001": {"owner": "Manoj Kumar", "type": "Savings", "balance": 152430.75, "currency": "INR"},
    "ACC1002": {"owner": "Manoj Kumar", "type": "Current", "balance": 48200.00, "currency": "INR"},
}


def get_account_balance(account_id: str) -> dict:
    """Fetches the current balance for a given bank account.

    Args:
        account_id: The account identifier, e.g. "ACC1001".

    Returns:
        A dict with status and either the balance details or an error message.
    """
    account = _MOCK_ACCOUNTS.get(account_id.upper())
    if not account:
        return {"status": "error", "message": f"No account found with id '{account_id}'."}
    return {
        "status": "success",
        "account_id": account_id.upper(),
        "owner": account["owner"],
        "type": account["type"],
        "balance": account["balance"],
        "currency": account["currency"],
    }


def list_accounts(owner_name: str) -> dict:
    """Lists all accounts belonging to a given account holder name.

    Args:
        owner_name: The name of the account holder.

    Returns:
        A dict with status and a list of matching accounts.
    """
    matches = [
        {"account_id": acc_id, **details}
        for acc_id, details in _MOCK_ACCOUNTS.items()
        if details["owner"].lower() == owner_name.lower()
    ]
    if not matches:
        return {"status": "error", "message": f"No accounts found for '{owner_name}'."}
    return {"status": "success", "accounts": matches}


balance_agent = LlmAgent(
    name="balance_agent",
    #model="gemini-2.5-flash",
    model=ModelManager.get_model(),
    description=(
        "Handles questions about account balances, account types, and "
        "listing accounts owned by a customer. Does NOT handle transaction "
        "history or fraud reports."
    ),
    instruction=(
        "You are a banking balance specialist. Use the `get_account_balance` "
        "tool when the user asks about the balance of a specific account id. "
        "Use `list_accounts` when the user asks what accounts they have. "
        "Always confirm the account id and currency back to the user. "
        "If required info (like an account id) is missing, ask for it "
        "before calling a tool."
    ),
    tools=[get_account_balance, list_accounts],
)

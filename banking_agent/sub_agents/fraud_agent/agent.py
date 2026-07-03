"""Fraud & Disputes Agent

Handles reporting suspicious/fraudulent transactions and blocking cards.
This is the most sensitive sub-agent, so its instruction explicitly asks
for confirmation before taking any destructive action (e.g. blocking a card).
"""

from google.adk.agents import LlmAgent
from banking_agent.config.model_config import ModelManager

_MOCK_CASE_COUNTER = {"next_id": 5001}
_MOCK_CARD_STATUS = {"ACC1001": "ACTIVE", "ACC1002": "ACTIVE"}


def report_fraud(account_id: str, txn_id: str, reason: str) -> dict:
    """Files a fraud/dispute case for a specific transaction.

    Args:
        account_id: The account identifier the transaction belongs to.
        txn_id: The disputed transaction id.
        reason: A short description of why the transaction is disputed.

    Returns:
        A dict with status and the created case id.
    """
    case_id = f"CASE{_MOCK_CASE_COUNTER['next_id']}"
    _MOCK_CASE_COUNTER["next_id"] += 1
    return {
        "status": "success",
        "case_id": case_id,
        "account_id": account_id.upper(),
        "txn_id": txn_id.upper(),
        "reason": reason,
        "message": (
            f"Fraud case {case_id} has been filed for transaction {txn_id.upper()} "
            f"on account {account_id.upper()}. Our team will investigate within 3-5 business days."
        ),
    }


def block_card(account_id: str, confirm: bool) -> dict:
    """Blocks the debit/credit card linked to an account.

    Args:
        account_id: The account identifier whose card should be blocked.
        confirm: Must be True. This is a destructive action, so the calling
            agent must have explicitly confirmed with the user first.

    Returns:
        A dict with status of the block request.
    """
    if not confirm:
        return {
            "status": "error",
            "message": "Card block was not confirmed. Ask the user to explicitly confirm before retrying.",
        }
    account_id = account_id.upper()
    if account_id not in _MOCK_CARD_STATUS:
        return {"status": "error", "message": f"No account found with id '{account_id}'."}
    _MOCK_CARD_STATUS[account_id] = "BLOCKED"
    return {"status": "success", "account_id": account_id, "card_status": "BLOCKED"}


fraud_agent = LlmAgent(
    name="fraud_agent",
    #model="gemini-2.5-flash",
    model=ModelManager.get_model(),
    description=(
        "Handles reporting fraudulent or suspicious transactions and blocking "
        "a lost/compromised card. Does NOT handle balance or general "
        "transaction-history lookups."
    ),
    instruction=(
        "You are a banking fraud & disputes specialist. "
        "When a user wants to dispute a transaction, use `report_fraud` with "
        "the account id, transaction id, and their stated reason. "
        "Blocking a card is destructive: before calling `block_card`, "
        "explicitly ask the user 'Are you sure you want to block the card on "
        "account <id>? This cannot be undone immediately.' and only call the "
        "tool with confirm=True after they clearly say yes. "
        "Be calm and reassuring, since users contacting you may be stressed "
        "about potential fraud."
    ),
    tools=[report_fraud, block_card],
)

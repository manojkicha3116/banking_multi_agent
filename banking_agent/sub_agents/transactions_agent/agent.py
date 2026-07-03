"""Transactions Agent

Handles queries about transaction history and statements.
"""

from google.adk.agents import LlmAgent
from banking_agent.config.model_config import ModelManager

# --- Mock transaction ledger --------------------------------------------
_MOCK_TRANSACTIONS = {
    "ACC1001": [
        {"txn_id": "TXN9001", "date": "2026-06-25", "description": "UPI - Swiggy", "amount": -540.00},
        {"txn_id": "TXN9002", "date": "2026-06-27", "description": "Salary Credit", "amount": 95000.00},
        {"txn_id": "TXN9003", "date": "2026-06-29", "description": "NEFT to ACC1002", "amount": -10000.00},
    ],
    "ACC1002": [
        {"txn_id": "TXN9101", "date": "2026-06-29", "description": "NEFT from ACC1001", "amount": 10000.00},
        {"txn_id": "TXN9102", "date": "2026-06-30", "description": "ATM Withdrawal", "amount": -2000.00},
    ],
}


def get_transaction_history(account_id: str, limit: int = 5) -> dict:
    """Fetches recent transactions for an account.

    Args:
        account_id: The account identifier, e.g. "ACC1001".
        limit: Maximum number of recent transactions to return.

    Returns:
        A dict with status and a list of transactions (most recent last).
    """
    txns = _MOCK_TRANSACTIONS.get(account_id.upper())
    if txns is None:
        return {"status": "error", "message": f"No account found with id '{account_id}'."}
    return {"status": "success", "account_id": account_id.upper(), "transactions": txns[-limit:]}


def find_transaction(account_id: str, txn_id: str) -> dict:
    """Looks up a single transaction by id within an account.

    Args:
        account_id: The account identifier.
        txn_id: The transaction identifier, e.g. "TXN9001".

    Returns:
        A dict with status and the transaction details if found.
    """
    txns = _MOCK_TRANSACTIONS.get(account_id.upper(), [])
    for txn in txns:
        if txn["txn_id"].upper() == txn_id.upper():
            return {"status": "success", "transaction": txn}
    return {"status": "error", "message": f"Transaction '{txn_id}' not found in account '{account_id}'."}


transactions_agent = LlmAgent(
    name="transactions_agent",
    #model="gemini-2.5-flash",
    model=ModelManager.get_model(),
    description=(
        "Handles questions about transaction history, statements, and "
        "looking up a specific transaction by id. Does NOT handle balances "
        "or fraud disputes."
    ),
    instruction=(
        "You are a banking transactions specialist. Use `get_transaction_history` "
        "to list recent transactions for an account, and `find_transaction` to "
        "look up one specific transaction id. Present amounts with a '+' for "
        "credits and '-' for debits. If the account id is missing, ask for it."
    ),
    tools=[get_transaction_history, find_transaction],
)

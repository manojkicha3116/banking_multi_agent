# Banking Multi-Agent Sample (Google ADK)

A minimal multi-agent banking assistant built with the Agent Development Kit (ADK).
A `banking_coordinator` root agent routes each user request to one of three
specialist sub-agents, using ADK's LLM-driven delegation (AutoFlow):

```
banking_coordinator (root)
├── balance_agent        -> account balances, list accounts
├── transactions_agent   -> transaction history, look up a transaction
└── fraud_agent          -> report fraud/dispute a charge, block a card
```

Each sub-agent owns its own tools (plain Python functions ADK auto-wraps as
`FunctionTool`s) and mock data, so the sample runs with no external banking
system or database — swap the mock dicts in each `agent.py` for real API/DB
calls when you're ready.

## Project layout

```
banking_multi_agent/
├── banking_agent/
│   ├── __init__.py          # exposes root_agent
│   ├── agent.py              # coordinator / root agent
│   └── sub_agents/
│       ├── balance_agent/
│       ├── transactions_agent/
│       └── fraud_agent/
├── main.py                   # standalone script to test without adk CLI
├── requirements.txt
└── .env.example
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env and add your GOOGLE_API_KEY (get one at https://aistudio.google.com/apikey)
```

## Run it

**Option 1 — ADK web UI** (recommended for exploring, run from the folder containing `banking_agent/`):
```bash
adk web
```

**Option 2 — ADK interactive CLI:**
```bash
adk run banking_agent
```

**Option 3 — plain Python script:**
```bash
python main.py
```

## Try these prompts
- "What's the balance on ACC1001?"
- "List all accounts for Manoj Kumar"
- "Show my last 5 transactions on ACC1001"
- "I don't recognize TXN9001, please dispute it"
- "Block the card on ACC1001" (fraud_agent will ask you to confirm first)

## Extending this sample
- Replace the mock dicts with real calls to a core-banking API.
- Add a `SequentialAgent` (e.g. verify identity -> then route) in front of the coordinator.
- Add an `AgentTool`-wrapped compliance/PII-redaction agent if you need it in
  regulated environments.
- Swap `model="gemini-2.5-flash"` per agent for different cost/latency tradeoffs.

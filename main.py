"""Standalone runner for the banking multi-agent sample.

This lets you try the agent from the terminal without using `adk web`/`adk run`.

Usage:
    python main.py
"""

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from banking_agent.agent import root_agent

APP_NAME = "banking_multi_agent"
USER_ID = "demo_user"


async def ask(runner: Runner, session_id: str, message: str) -> None:
    print(f"\nUSER: {message}")
    user_content = types.Content(role="user", parts=[types.Part(text=message)])
    async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
        if event.is_final_response() and event.content and event.content.parts:
            text = "".join(p.text for p in event.content.parts if p.text)
            if text:
                print(f"AGENT: {text}")


async def main() -> None:
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    # A few sample turns showing routing to each specialist sub-agent.
    await ask(runner, session.id, "Hi, what's the balance on ACC1001?")
    await ask(runner, session.id, "Can you show my last 3 transactions on that account?")
    await ask(runner, session.id, "I don't recognize TXN9001, I think it's fraud. Please dispute it.")


if __name__ == "__main__":
    asyncio.run(main())

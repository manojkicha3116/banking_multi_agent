from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from banking_agent.agent import root_agent

APP_NAME = "banking_multi_agent"
USER_ID = "demo_user"


class ADKService:

    def __init__(self):
        self.session_service = InMemorySessionService()

        self.runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=self.session_service,
        )

    async def create_session(self):

        session = await self.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
        )

        return session.id

    async def ask(self, session_id: str, query: str):

        user_content = types.Content(
            role="user",
            parts=[types.Part(text=query)],
        )

        answer = ""

        async for event in self.runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=user_content,
        ):

            if event.is_final_response():
                if event.content and event.content.parts:
                    answer = "".join(
                        part.text
                        for part in event.content.parts
                        if part.text
                    )

        return answer


adk_service = ADKService()
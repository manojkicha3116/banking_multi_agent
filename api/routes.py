from fastapi import APIRouter

from banking_agent.adk_service import adk_service
from schemas.request import QueryRequest
from schemas.response import QueryResponse

router = APIRouter()


@router.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):

    session_id = request.session_id

    if session_id is None:
        session_id = await adk_service.create_session()

    response = await adk_service.ask(
        session_id=session_id,
        query=request.query,
    )

    return QueryResponse(
        session_id=session_id,
        response=response,
    )
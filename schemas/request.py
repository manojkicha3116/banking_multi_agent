from pydantic import BaseModel

class QueryRequest(BaseModel):
    """
    Purpose of this method is to initialize a request model
    """
    query: str
    session_id: str | None = None
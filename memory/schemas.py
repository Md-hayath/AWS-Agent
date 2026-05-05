from pydantic import BaseModel
from typing import List, Any

class AgentState(BaseModel):
    messages: List[Any]

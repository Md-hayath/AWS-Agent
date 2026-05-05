from pydantic import BaseModel
from typing import List, Any, Optional

class ExecutionState(BaseModel):
    current_step: int = 0
    plan: List[str] = []
    status: str = "idle"
    context: Optional[dict] = {}

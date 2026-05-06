from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from workflows.chat_agent import ChatWorkflow

app = FastAPI(title="AWS DevOps AI Agent")

# Initialize once
try:
    workflow = ChatWorkflow()
except Exception as e:
    raise RuntimeError(f"Workflow init failed: {e}")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/chat")
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    try:
        response = workflow.run(req.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
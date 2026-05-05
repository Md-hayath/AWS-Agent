from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.dependencies import get_chat_workflow
from workflows.chat_agent import ChatWorkflow

app = FastAPI(title="AWS DevOps AI Agent API")

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str

@app.post("/chat", response_model=PromptResponse)
def chat_endpoint(request: PromptRequest, workflow: ChatWorkflow = Depends(get_chat_workflow)):
    """API Endpoint to chat with the AWS Agent."""
    response_text = workflow.run(request.prompt)
    return PromptResponse(response=response_text)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

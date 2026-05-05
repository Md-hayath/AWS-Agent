from workflows.chat_agent import ChatWorkflow

# FastAPI Dependency Injection
def get_chat_workflow():
    # Return a singleton or new instance depending on requirements
    return ChatWorkflow()

from memory.schemas import AgentState
from langchain_core.messages import HumanMessage, AIMessage

class AgentMemory:
    def __init__(self):
        self.state = AgentState(messages=[])

    def add_human_message(self, content: str):
        self.state.messages.append(HumanMessage(content=content))

    def add_ai_message(self, content: str):
        self.state.messages.append(AIMessage(content=content))
        
    def get_history(self):
        return self.state.messages

from agent.agent import create_aws_agent
from langchain_core.messages import HumanMessage, AIMessage

class ResearchWorkflow:
    def __init__(self):
        self.agent_executor = create_aws_agent()
        
    def research(self, topic: str) -> str:
        """A specialized workflow for researching AWS best practices before deploying."""
        prompt = f"Research the following AWS topic and provide best practices: {topic}. Do not execute modifying commands."
        response = self.agent_executor.invoke({
            "input": prompt,
            "chat_history": []
        })
        return response.get("output", "No research found.")

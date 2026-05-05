from agent.agent import create_aws_agent
from langchain_core.messages import HumanMessage
from utils.logger import logger

class ChatWorkflow:
    def __init__(self):
        self.agent_executor = create_aws_agent()
        self.chat_history = []

    def run(self, user_input: str) -> str:
        logger.info(f"User Input: {user_input}")
        
        try:
            self.chat_history.append(HumanMessage(content=user_input))
            
            # Invoke the LangGraph agent
            response = self.agent_executor.invoke({
                "messages": self.chat_history
            })
            
            # The response contains all messages including tool calls and outputs
            final_messages = response.get("messages", [])
            output = final_messages[-1].content if final_messages else "No response generated."
            
            # Sync our history with the graph's history
            self.chat_history = final_messages
            
            return output
        except Exception as e:
            logger.error(f"Error executing agent: {str(e)}")
            return f"An error occurred: {str(e)}"

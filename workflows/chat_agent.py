from agent.agent import create_aws_agent
from utils.logger import logger
import traceback


class ChatWorkflow:
    def __init__(self):
        self.agent_executor = create_aws_agent()

        logger.info("ChatWorkflow initialized successfully")

    def run(self, user_input: str) -> str:
        logger.info(f"User Input: {user_input}")

        try:
            response = self.agent_executor.invoke({
                "input": user_input
            })

            logger.debug(f"Raw agent response: {response}")

            output = response.get("output", "No response generated.")
            return output

        except Exception as e:
            import traceback
            logger.error("Error executing agent")
            traceback.print_exc()
            return f"REAL ERROR: {str(e)}"

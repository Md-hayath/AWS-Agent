from agent.agent import create_aws_agent

class AgentExecuter:
    def __init__(self):
        self.executor = create_aws_agent()

    def execute_task(self, task: str, context: dict = None):
        """Executes a specific AWS task."""
        if context is None:
            context = {}
        return self.executor.invoke({"input": task, "chat_history": context.get("chat_history", [])})

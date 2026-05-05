class AgentPlanner:
    def __init__(self, llm):
        self.llm = llm

    def plan(self, objective: str):
        """Generates a step-by-step plan for complex AWS deployments."""
        prompt = f"Create a step-by-step AWS deployment plan for the following objective: {objective}"
        # Simplified planning logic
        response = self.llm.invoke(prompt)
        return response.content

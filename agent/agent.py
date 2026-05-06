from llm.client import get_llm
from llm.prompts import SYSTEM_PROMPT
from tools.custom_tools import all_aws_tools
from langchain.agents import initialize_agent, AgentType
from langchain_core.messages import SystemMessage


def create_aws_agent():
    llm = get_llm()

    agent = initialize_agent(
        tools=all_aws_tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=False,
        agent_kwargs={
            "system_message": SystemMessage(content=SYSTEM_PROMPT)
        }
    )

    return agent

"""from langgraph.prebuilt import create_react_agent
from llm.client import get_llm
from llm.prompts import SYSTEM_PROMPT
from tools.custom_tools import all_aws_tools

def create_aws_agent():
    llm = get_llm()
    
    # We use LangGraph's prebuilt react agent which is the modern standard
    agent_executor = create_react_agent(
        llm, 
        tools=all_aws_tools, 
        messages_modifier=SYSTEM_PROMPT
    )
    
    return agent_executor"""

from langgraph.prebuilt import create_react_agent
from llm.client import get_llm
from tools.custom_tools import all_aws_tools


def create_aws_agent():
    llm = get_llm()

    # Create the agent WITHOUT unsupported arguments
    agent_executor = create_react_agent(
        llm,
        tools=all_aws_tools
    )

    return agent_executor

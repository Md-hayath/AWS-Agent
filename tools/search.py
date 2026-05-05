from langchain_core.tools import tool

@tool
def search_aws_docs(query: str) -> str:
    """Search AWS documentation for a given query."""
    return f"Simulated search results for '{query}': AWS Docs recommend configuring IAM roles with least privilege."

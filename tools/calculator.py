from langchain_core.tools import tool

@tool
def calculate_cost(instance_type: str, hours: int) -> str:
    """Mock tool to estimate EC2 costs based on instance type and usage hours."""
    # Dummy rates
    rates = {
        "t2.micro": 0.0116,
        "t2.large": 0.0928,
        "m5.large": 0.096
    }
    rate = rates.get(instance_type, 0.1)
    cost = rate * hours
    return f"Estimated cost for {instance_type} running {hours} hours is ${cost:.2f}"

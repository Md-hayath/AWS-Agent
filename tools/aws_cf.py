import json
from langchain_core.tools import tool
from tools.base import get_boto3_client
from utils.retry import retry_aws_call

@tool
@retry_aws_call()
def aws_create_stack(stack_name: str, template_body: str) -> str:
    """Create a CloudFormation stack using a template string."""
    client = get_boto3_client("cloudformation")
    client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM']
    )
    return f"Creating stack {stack_name} initiated."

@tool
@retry_aws_call()
def aws_update_stack(stack_name: str, template_body: str) -> str:
    """Update an existing CloudFormation stack."""
    client = get_boto3_client("cloudformation")
    client.update_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM']
    )
    return f"Updating stack {stack_name} initiated."

@tool
@retry_aws_call()
def aws_delete_stack(stack_name: str) -> str:
    """Delete a CloudFormation stack."""
    client = get_boto3_client("cloudformation")
    client.delete_stack(StackName=stack_name)
    return f"Deleting stack {stack_name} initiated."

@tool
@retry_aws_call()
def aws_describe_stacks(stack_name: str = None) -> str:
    """Describe CloudFormation stacks. Provide stack_name for a specific stack, or None for all."""
    client = get_boto3_client("cloudformation")
    kwargs = {}
    if stack_name:
        kwargs['StackName'] = stack_name
    response = client.describe_stacks(**kwargs)
    stacks = [{"StackName": s["StackName"], "StackStatus": s["StackStatus"]} for s in response.get("Stacks", [])]
    return json.dumps(stacks)

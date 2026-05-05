import json
from langchain_core.tools import tool
from tools.base import get_boto3_client
from utils.retry import retry_aws_call

# --- IAM ---

@tool
@retry_aws_call()
def aws_create_user(user_name: str) -> str:
    """Create a new IAM user."""
    client = get_boto3_client("iam")
    client.create_user(UserName=user_name)
    return f"IAM User {user_name} created."

@tool
@retry_aws_call()
def aws_delete_user(user_name: str) -> str:
    """Delete an IAM user."""
    client = get_boto3_client("iam")
    client.delete_user(UserName=user_name)
    return f"IAM User {user_name} deleted."

@tool
@retry_aws_call()
def aws_attach_user_policy(user_name: str, policy_arn: str) -> str:
    """Attach a managed policy to an IAM user."""
    client = get_boto3_client("iam")
    client.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
    return f"Attached policy {policy_arn} to {user_name}."

@tool
@retry_aws_call()
def aws_list_roles() -> str:
    """List IAM roles."""
    client = get_boto3_client("iam")
    response = client.list_roles()
    roles = [role['RoleName'] for role in response.get('Roles', [])]
    return json.dumps(roles)

@tool
@retry_aws_call()
def aws_pass_role(role_name: str) -> str:
    """Note: pass_role is an IAM permission, not an API call. Returning info about it."""
    return f"iam:PassRole is a permission. To pass {role_name}, attach a policy allowing iam:PassRole on it."

# --- STS ---

@tool
@retry_aws_call()
def aws_assume_role(role_arn: str, role_session_name: str) -> str:
    """Assume an IAM role and return temporary credentials."""
    client = get_boto3_client("sts")
    response = client.assume_role(RoleArn=role_arn, RoleSessionName=role_session_name)
    creds = response['Credentials']
    # Not returning secret key to the LLM directly for security reasons, just confirmation
    return f"Assumed role {role_arn}. AccessKeyId: {creds['AccessKeyId']}. Note: Agent cannot use these temp creds directly yet."

@tool
@retry_aws_call()
def aws_get_caller_identity() -> str:
    """Get details about the current IAM principal making the API calls."""
    client = get_boto3_client("sts")
    response = client.get_caller_identity()
    return f"Account: {response.get('Account')}, Arn: {response.get('Arn')}, UserId: {response.get('UserId')}"

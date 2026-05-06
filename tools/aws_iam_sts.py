import json
from langchain_core.tools import tool
from tools.base import get_boto3_client
from utils.retry import retry_aws_call
POLICY_ARN_MAP = {
    "admin": "arn:aws:iam::aws:policy/AdministratorAccess",
    "eks_readonly": "arn:aws:iam::aws:policy/AmazonEKSReadOnlyAccess",
    "readonly": "arn:aws:iam::aws:policy/ReadOnlyAccess",
    # Add more policy mappings as needed
}

# --- IAM ---

@tool
@retry_aws_call()
def aws_list_users() -> str:
    """List IAM users in the AWS account, including user name, ARN, user ID, and creation date."""
    client = get_boto3_client("iam")
    users = []
    paginator = client.get_paginator("list_users")

    for page in paginator.paginate():
        for user in page.get("Users", []):
            users.append({
                "UserName": user.get("UserName"),
                "UserId": user.get("UserId"),
                "Arn": user.get("Arn"),
                "CreateDate": user.get("CreateDate"),
            })

    return json.dumps(users, default=str)


@tool
@retry_aws_call()
def aws_create_user(user_name: str) -> str:
    """Create a new IAM user and return its ARN."""
    client = get_boto3_client("iam")
    response = client.create_user(UserName=user_name)
    return response.get('User', {}).get('Arn', f"IAM User {user_name} created.")

@tool
@retry_aws_call()
def aws_create_user_with_policy(user_name: str, policy_key: str) -> str:
    """Create IAM user, attach a managed policy, create access key, and return credentials.
    policy_key should match keys in POLICY_ARN_MAP (e.g., 'admin', 'eks_readonly', 'readonly')."""
    client = get_boto3_client("iam")
    # Create user
    resp = client.create_user(UserName=user_name)
    user_arn = resp.get('User', {}).get('Arn')
    # Resolve policy ARN
    policy_arn = POLICY_ARN_MAP.get(policy_key)
    if not policy_arn:
        return f"Policy key '{policy_key}' not recognized. Available keys: {list(POLICY_ARN_MAP.keys())}."
    # Attach policy
    client.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
    # Create access key
    access_key_info = client.create_access_key(UserName=user_name).get('AccessKey', {})
    credentials = {
        "UserName": user_name,
        "UserArn": user_arn,
        "AccessKeyId": access_key_info.get('AccessKeyId'),
        "SecretAccessKey": access_key_info.get('SecretAccessKey'),
        "PolicyArn": policy_arn
    }
    return json.dumps(credentials)

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

import uuid

def generate_session_id() -> str:
    """Generate a unique session ID for tracking requests."""
    return str(uuid.uuid4())

def format_aws_arn(service: str, region: str, account_id: str, resource: str) -> str:
    """Helper to format AWS ARNs."""
    return f"arn:aws:{service}:{region}:{account_id}:{resource}"

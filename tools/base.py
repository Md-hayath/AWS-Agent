import boto3
from app.config import config

def get_boto3_client(service_name: str, region_name: str = None):
    """
    Returns a boto3 client for the given service.
    Uses credentials from environment or defaults to host config.
    """
    kwargs = {}
    if region_name:
        kwargs['region_name'] = region_name
    elif config.aws_default_region:
        kwargs['region_name'] = config.aws_default_region

    if config.aws_access_key_id and config.aws_secret_access_key:
        kwargs['aws_access_key_id'] = config.aws_access_key_id
        kwargs['aws_secret_access_key'] = config.aws_secret_access_key

    return boto3.client(service_name, **kwargs)

def get_boto3_resource(service_name: str, region_name: str = None):
    """
    Returns a boto3 resource.
    """
    kwargs = {}
    if region_name:
        kwargs['region_name'] = region_name
    elif config.aws_default_region:
        kwargs['region_name'] = config.aws_default_region

    if config.aws_access_key_id and config.aws_secret_access_key:
        kwargs['aws_access_key_id'] = config.aws_access_key_id
        kwargs['aws_secret_access_key'] = config.aws_secret_access_key

    return boto3.resource(service_name, **kwargs)

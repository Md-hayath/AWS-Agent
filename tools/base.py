import boto3
import os
from app.config import config


def get_boto3_client(service_name: str, region_name: str = None):
    """
    Returns a boto3 client for the given service.
    Priority:
    1. Explicit config values
    2. Environment variables
    3. Default boto3 chain (CLI/IAM)
    """

    region = (
        region_name
        or getattr(config, "aws_default_region", None)
        or os.getenv("AWS_DEFAULT_REGION")
    )

    access_key = (
        getattr(config, "aws_access_key_id", None)
        or os.getenv("AWS_ACCESS_KEY_ID")
    )

    secret_key = (
        getattr(config, "aws_secret_access_key", None)
        or os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    kwargs = {"region_name": region} if region else {}

    if access_key and secret_key:
        kwargs.update({
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key
        })

    print(f"[DEBUG] granting request {service_name} client | Region: {region} | Key Present: {bool(access_key)}")

    return boto3.client(service_name, **kwargs)


def get_boto3_resource(service_name: str, region_name: str = None):
    """
    Returns a boto3 resource with same fallback logic.
    """

    region = (
        region_name
        or getattr(config, "aws_default_region", None)
        or os.getenv("AWS_DEFAULT_REGION")
    )

    access_key = (
        getattr(config, "aws_access_key_id", None)
        or os.getenv("AWS_ACCESS_KEY_ID")
    )

    secret_key = (
        getattr(config, "aws_secret_access_key", None)
        or os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    kwargs = {"region_name": region} if region else {}

    if access_key and secret_key:
        kwargs.update({
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key
        })

    print(f"[DEBUG] Creating {service_name} resource | Region: {region} | Key Present: {bool(access_key)}")

    return boto3.resource(service_name, **kwargs)
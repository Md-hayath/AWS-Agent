import json
from langchain_core.tools import tool
from tools.base import get_boto3_client
from utils.retry import retry_aws_call


@tool
@retry_aws_call()
def aws_list_buckets() -> str:
    """List all S3 buckets in the AWS account."""
    client = get_boto3_client("s3")
    response = client.list_buckets()
    buckets = [bucket["Name"] for bucket in response.get("Buckets", [])]
    return json.dumps(buckets)


@tool
@retry_aws_call()
def aws_create_bucket(bucket_name: str, region: str = None) -> str:
    """
    Create an S3 bucket.
    Args:
        bucket_name: globally unique bucket name
        region: AWS region (optional, defaults to configured region)
    """
    client = get_boto3_client("s3", region_name=region)

    actual_region = region or client.meta.region_name
    kwargs = {"Bucket": bucket_name}

    # S3 special case: us-east-1 does NOT need LocationConstraint
    if actual_region != "us-east-1":
        kwargs["CreateBucketConfiguration"] = {
            "LocationConstraint": actual_region
        }

    client.create_bucket(**kwargs)
    return f"Bucket '{bucket_name}' created in {actual_region}."


@tool
@retry_aws_call()
def aws_delete_bucket(bucket_name: str) -> str:
    """
    Delete an S3 bucket.
    Note: bucket must be empty.
    """
    client = get_boto3_client("s3")
    client.delete_bucket(Bucket=bucket_name)
    return f"Bucket '{bucket_name}' deleted."


@tool
@retry_aws_call()
def aws_list_objects(bucket_name: str, prefix: str = "") -> str:
    """
    List objects in a bucket.
    Args:
        bucket_name: target bucket
        prefix: filter objects by prefix (optional)
    """
    client = get_boto3_client("s3")

    response = client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix
    )

    objects = [obj["Key"] for obj in response.get("Contents", [])]
    return json.dumps(objects)


@tool
@retry_aws_call()
def aws_get_object(bucket_name: str, object_key: str) -> str:
    """
    Get object content from S3 (text only).
    """
    client = get_boto3_client("s3")

    response = client.get_object(
        Bucket=bucket_name,
        Key=object_key
    )

    content = response["Body"].read().decode("utf-8")
    return content


@tool
@retry_aws_call()
def aws_put_object(bucket_name: str, object_key: str, content: str) -> str:
    """
    Upload text content to S3.
    """
    client = get_boto3_client("s3")

    client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=content.encode("utf-8")
    )

    return f"Object '{object_key}' uploaded to '{bucket_name}'."


@tool
@retry_aws_call()
def aws_delete_object(bucket_name: str, object_key: str) -> str:
    """
    Delete an object from S3.
    """
    client = get_boto3_client("s3")

    client.delete_object(
        Bucket=bucket_name,
        Key=object_key
    )
    return f"Object '{object_key}' deleted from '{bucket_name}'."

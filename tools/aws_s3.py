import json
from langchain_core.tools import tool
from tools.base import get_boto3_client
from utils.logger import logger
from utils.retry import retry_aws_call

@tool
@retry_aws_call()
def aws_list_buckets() -> str:
    """List all S3 buckets in the AWS account."""
    client = get_boto3_client("s3")
    response = client.list_buckets()
    buckets = [bucket['Name'] for bucket in response.get('Buckets', [])]
    return json.dumps(buckets)

@tool
@retry_aws_call()
def aws_create_bucket(bucket_name: str, region: str = None) -> str:
    """Create an S3 bucket. Requires a unique bucket_name."""
    client = get_boto3_client("s3", region_name=region)
    kwargs = {'Bucket': bucket_name}
    
    actual_region = region or client.meta.region_name
    if actual_region != 'us-east-1':
        kwargs['CreateBucketConfiguration'] = {'LocationConstraint': actual_region}
        
    client.create_bucket(**kwargs)
    return f"Bucket {bucket_name} created successfully."

@tool
@retry_aws_call()
def aws_delete_bucket(bucket_name: str) -> str:
    """Delete an empty S3 bucket."""
    client = get_boto3_client("s3")
    client.delete_bucket(Bucket=bucket_name)
    return f"Bucket {bucket_name} deleted successfully."

@tool
@retry_aws_call()
def aws_list_objects_v2(bucket_name: str, prefix: str = "") -> str:
    """List objects in an S3 bucket, optionally filtered by prefix."""
    client = get_boto3_client("s3")
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    objects = [obj['Key'] for obj in response.get('Contents', [])]
    return json.dumps(objects)

@tool
@retry_aws_call()
def aws_get_object(bucket_name: str, object_key: str) -> str:
    """Get the string content of an object from S3."""
    client = get_boto3_client("s3")
    response = client.get_object(Bucket=bucket_name, Key=object_key)
    content = response['Body'].read().decode('utf-8')
    return content

@tool
@retry_aws_call()
def aws_put_object(bucket_name: str, object_key: str, content: str) -> str:
    """Put string content into an S3 object."""
    client = get_boto3_client("s3")
    client.put_object(Bucket=bucket_name, Key=object_key, Body=content.encode('utf-8'))
    return f"Object {object_key} uploaded to {bucket_name}."

@tool
@retry_aws_call()
def aws_delete_object(bucket_name: str, object_key: str) -> str:
    """Delete an object from an S3 bucket."""
    client = get_boto3_client("s3")
    client.delete_object(Bucket=bucket_name, Key=object_key)
    return f"Object {object_key} deleted from {bucket_name}."

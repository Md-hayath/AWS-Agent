import json
from langchain_core.tools import tool
from tools.base import get_boto3_client
from utils.retry import retry_aws_call

@tool
@retry_aws_call()
def aws_describe_instances() -> str:
    """Describe all EC2 instances and return their IDs and states."""
    client = get_boto3_client("ec2")
    response = client.describe_instances()
    instances = []
    for reservation in response.get('Reservations', []):
        for inst in reservation.get('Instances', []):
            instances.append({
                "InstanceId": inst.get("InstanceId"),
                "State": inst.get("State", {}).get("Name"),
                "InstanceType": inst.get("InstanceType")
            })
    return json.dumps(instances)

@tool
@retry_aws_call()
def aws_run_instances(image_id: str, instance_type: str, min_count: int = 1, max_count: int = 1) -> str:
    """Launch new EC2 instances."""
    client = get_boto3_client("ec2")
    response = client.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        MinCount=min_count,
        MaxCount=max_count
    )
    instances = [inst['InstanceId'] for inst in response.get('Instances', [])]
    return f"Started instances: {instances}"

@tool
@retry_aws_call()
def aws_stop_instances(instance_ids: list[str]) -> str:
    """Stop one or more EC2 instances."""
    client = get_boto3_client("ec2")
    client.stop_instances(InstanceIds=instance_ids)
    return f"Stopping instances: {instance_ids}"

@tool
@retry_aws_call()
def aws_start_instances(instance_ids: list[str]) -> str:
    """Start one or more stopped EC2 instances."""
    client = get_boto3_client("ec2")
    client.start_instances(InstanceIds=instance_ids)
    return f"Starting instances: {instance_ids}"

@tool
@retry_aws_call()
def aws_terminate_instances(instance_ids: list[str]) -> str:
    """Terminate one or more EC2 instances."""
    client = get_boto3_client("ec2")
    client.terminate_instances(InstanceIds=instance_ids)
    return f"Terminating instances: {instance_ids}"

@tool
@retry_aws_call()
def aws_describe_images(owners: list[str] = ['self']) -> str:
    """Describe AMIs (Amazon Machine Images). Owners can be 'self', 'amazon', etc."""
    client = get_boto3_client("ec2")
    response = client.describe_images(Owners=owners)
    images = [{"ImageId": img["ImageId"], "Name": img.get("Name", "N/A")} for img in response.get("Images", [])]
    return json.dumps(images[:10]) # Return max 10 to avoid huge payload

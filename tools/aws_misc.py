import json
import datetime
from langchain_core.tools import tool
from tools.base import get_boto3_client
from utils.retry import retry_aws_call

# --- CloudWatch ---
@tool
@retry_aws_call()
def aws_get_metric_data(metric_name: str, namespace: str) -> str:
    """Mock-like implementation to get metric data for simplicity. Usually needs complex querying."""
    return f"Fetching metric {metric_name} in {namespace} is complex, requires start/end times and queries."

@tool
@retry_aws_call()
def aws_describe_alarms() -> str:
    """Describe CloudWatch Alarms."""
    client = get_boto3_client("cloudwatch")
    response = client.describe_alarms()
    alarms = [a['AlarmName'] for a in response.get('MetricAlarms', [])]
    return json.dumps(alarms)

# --- Lambda ---
@tool
@retry_aws_call()
def aws_create_function(function_name: str, role_arn: str, handler: str, runtime: str) -> str:
    """Dummy logic for create_function. Real implementation needs zip file."""
    return f"To create lambda {function_name}, we need a zip file. Use boto3 direct script."

@tool
@retry_aws_call()
def aws_invoke(function_name: str, payload: str) -> str:
    """Invoke a lambda function."""
    client = get_boto3_client("lambda")
    response = client.invoke(FunctionName=function_name, Payload=payload)
    return response['Payload'].read().decode('utf-8')

# --- DynamoDB ---
@tool
@retry_aws_call()
def aws_create_table(table_name: str, partition_key: str) -> str:
    """Create a simple DynamoDB table."""
    client = get_boto3_client("dynamodb")
    client.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': partition_key, 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': partition_key, 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    return f"Creating table {table_name} initiated."

@tool
@retry_aws_call()
def aws_put_item(table_name: str, item_json: str) -> str:
    """Put an item into DynamoDB. item_json must be valid JSON matching Boto3 format or simple dict."""
    client = get_boto3_client("dynamodb")
    client.put_item(TableName=table_name, Item=json.loads(item_json))
    return f"Item put into {table_name}."

# --- SNS ---
@tool
@retry_aws_call()
def aws_create_topic(name: str) -> str:
    """Create SNS topic."""
    client = get_boto3_client("sns")
    res = client.create_topic(Name=name)
    return f"Created topic ARN: {res.get('TopicArn')}"

@tool
@retry_aws_call()
def aws_publish(topic_arn: str, message: str) -> str:
    """Publish to SNS topic."""
    client = get_boto3_client("sns")
    client.publish(TopicArn=topic_arn, Message=message)
    return "Message published."

# --- SQS ---
@tool
@retry_aws_call()
def aws_create_queue(queue_name: str) -> str:
    """Create SQS queue."""
    client = get_boto3_client("sqs")
    res = client.create_queue(QueueName=queue_name)
    return f"Created queue URL: {res.get('QueueUrl')}"

@tool
@retry_aws_call()
def aws_send_message(queue_url: str, message_body: str) -> str:
    """Send message to SQS."""
    client = get_boto3_client("sqs")
    client.send_message(QueueUrl=queue_url, MessageBody=message_body)
    return "Message sent to queue."

# --- Bedrock ---
@tool
@retry_aws_call()
def aws_list_foundation_models() -> str:
    """List Bedrock foundation models."""
    client = get_boto3_client("bedrock")
    response = client.list_foundation_models()
    models = [m['modelId'] for m in response.get('modelSummaries', [])]
    return json.dumps(models)

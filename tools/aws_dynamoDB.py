import json
from decimal import Decimal
from typing import Optional

from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from langchain_core.tools import tool

from tools.base import get_boto3_client
from utils.retry import retry_aws_call


_SERIALIZER = TypeSerializer()
_DESERIALIZER = TypeDeserializer()
_ATTRIBUTE_VALUE_KEYS = {"S", "N", "B", "SS", "NS", "BS", "M", "L", "NULL", "BOOL"}


def _to_decimal(value):
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, list):
        return [_to_decimal(item) for item in value]
    if isinstance(value, dict):
        return {key: _to_decimal(item) for key, item in value.items()}
    return value


def _is_attribute_value(value) -> bool:
    return (
        isinstance(value, dict)
        and len(value) == 1
        and next(iter(value.keys())) in _ATTRIBUTE_VALUE_KEYS
    )


def _marshal_value(value):
    if _is_attribute_value(value):
        return value
    return _SERIALIZER.serialize(_to_decimal(value))


def _marshal_item(item: dict) -> dict:
    return {key: _marshal_value(value) for key, value in item.items()}


def _unmarshal_value(value):
    if not _is_attribute_value(value):
        return value
    return _DESERIALIZER.deserialize(value)


def _unmarshal_item(item: dict) -> dict:
    return {key: _unmarshal_value(value) for key, value in item.items()}


def _json_loads(value: Optional[str], default):
    if not value:
        return default
    return json.loads(value)


def _json_safe(value):
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    return value


def _to_json(data) -> str:
    return json.dumps(_json_safe(data), default=str)


@tool
@retry_aws_call()
def aws_create_table(
    table_name: str,
    partition_key: str,
    partition_key_type: str = "S",
    sort_key: Optional[str] = None,
    sort_key_type: str = "S",
    billing_mode: str = "PAY_PER_REQUEST",
    read_capacity_units: int = 5,
    write_capacity_units: int = 5,
) -> str:
    """Create a DynamoDB table. Supports a partition key and optional sort key. Key types are S, N, or B."""
    client = get_boto3_client("dynamodb")

    key_schema = [{"AttributeName": partition_key, "KeyType": "HASH"}]
    attribute_definitions = [
        {"AttributeName": partition_key, "AttributeType": partition_key_type}
    ]

    if sort_key:
        key_schema.append({"AttributeName": sort_key, "KeyType": "RANGE"})
        attribute_definitions.append({
            "AttributeName": sort_key,
            "AttributeType": sort_key_type,
        })

    kwargs = {
        "TableName": table_name,
        "KeySchema": key_schema,
        "AttributeDefinitions": attribute_definitions,
        "BillingMode": billing_mode,
    }

    if billing_mode == "PROVISIONED":
        kwargs["ProvisionedThroughput"] = {
            "ReadCapacityUnits": read_capacity_units,
            "WriteCapacityUnits": write_capacity_units,
        }

    response = client.create_table(**kwargs)
    table = response.get("TableDescription", {})

    return _to_json({
        "message": f"Creating DynamoDB table '{table_name}' started.",
        "tableName": table.get("TableName"),
        "tableStatus": table.get("TableStatus"),
        "tableArn": table.get("TableArn"),
    })


@tool
@retry_aws_call()
def aws_put_item(table_name: str, item_json: str) -> str:
    """Put an item into a DynamoDB table. item_json can be simple JSON or DynamoDB AttributeValue JSON."""
    client = get_boto3_client("dynamodb")
    item = _marshal_item(_json_loads(item_json, {}))

    client.put_item(TableName=table_name, Item=item)

    return f"Item written to DynamoDB table '{table_name}'."


@tool
@retry_aws_call()
def aws_get_item(table_name: str, key_json: str, consistent_read: bool = False) -> str:
    """Get one item from DynamoDB by primary key. key_json can be simple JSON or DynamoDB AttributeValue JSON."""
    client = get_boto3_client("dynamodb")
    key = _marshal_item(_json_loads(key_json, {}))

    response = client.get_item(
        TableName=table_name,
        Key=key,
        ConsistentRead=consistent_read,
    )

    item = response.get("Item")
    return _to_json({
        "found": item is not None,
        "item": _unmarshal_item(item) if item else None,
    })


@tool
@retry_aws_call()
def aws_query(
    table_name: str,
    key_condition_expression: str,
    expression_attribute_values_json: str,
    index_name: Optional[str] = None,
    filter_expression: Optional[str] = None,
    projection_expression: Optional[str] = None,
    expression_attribute_names_json: Optional[str] = None,
    scan_index_forward: bool = True,
    limit: Optional[int] = None,
) -> str:
    """Query DynamoDB using a key condition expression and expression values JSON."""
    client = get_boto3_client("dynamodb")

    kwargs = {
        "TableName": table_name,
        "KeyConditionExpression": key_condition_expression,
        "ExpressionAttributeValues": _marshal_item(
            _json_loads(expression_attribute_values_json, {})
        ),
        "ScanIndexForward": scan_index_forward,
    }

    if index_name:
        kwargs["IndexName"] = index_name
    if filter_expression:
        kwargs["FilterExpression"] = filter_expression
    if projection_expression:
        kwargs["ProjectionExpression"] = projection_expression
    if expression_attribute_names_json:
        kwargs["ExpressionAttributeNames"] = _json_loads(expression_attribute_names_json, {})
    if limit:
        kwargs["Limit"] = limit

    response = client.query(**kwargs)
    items = [_unmarshal_item(item) for item in response.get("Items", [])]

    return _to_json({
        "count": response.get("Count", 0),
        "scannedCount": response.get("ScannedCount", 0),
        "items": items,
        "lastEvaluatedKey": response.get("LastEvaluatedKey"),
    })


@tool
@retry_aws_call()
def aws_scan(
    table_name: str,
    filter_expression: Optional[str] = None,
    expression_attribute_values_json: Optional[str] = None,
    projection_expression: Optional[str] = None,
    expression_attribute_names_json: Optional[str] = None,
    limit: int = 25,
) -> str:
    """Scan a DynamoDB table. Use a small limit by default to avoid reading too much data."""
    client = get_boto3_client("dynamodb")

    kwargs = {
        "TableName": table_name,
        "Limit": limit,
    }

    if filter_expression:
        kwargs["FilterExpression"] = filter_expression
    if expression_attribute_values_json:
        kwargs["ExpressionAttributeValues"] = _marshal_item(
            _json_loads(expression_attribute_values_json, {})
        )
    if projection_expression:
        kwargs["ProjectionExpression"] = projection_expression
    if expression_attribute_names_json:
        kwargs["ExpressionAttributeNames"] = _json_loads(expression_attribute_names_json, {})

    response = client.scan(**kwargs)
    items = [_unmarshal_item(item) for item in response.get("Items", [])]

    return _to_json({
        "count": response.get("Count", 0),
        "scannedCount": response.get("ScannedCount", 0),
        "items": items,
        "lastEvaluatedKey": response.get("LastEvaluatedKey"),
    })


@tool
@retry_aws_call()
def aws_delete_item(table_name: str, key_json: str) -> str:
    """Delete one DynamoDB item by primary key. key_json can be simple JSON or DynamoDB AttributeValue JSON."""
    client = get_boto3_client("dynamodb")
    key = _marshal_item(_json_loads(key_json, {}))

    response = client.delete_item(
        TableName=table_name,
        Key=key,
        ReturnValues="ALL_OLD",
    )

    deleted_item = response.get("Attributes")
    return _to_json({
        "deleted": deleted_item is not None,
        "item": _unmarshal_item(deleted_item) if deleted_item else None,
    })

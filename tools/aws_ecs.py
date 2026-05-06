import json
from typing import Optional

from langchain_core.tools import tool

from tools.base import get_boto3_client
from utils.retry import retry_aws_call


def _to_json(data) -> str:
    return json.dumps(data, default=str)


def _short_arn(value: str) -> str:
    return value.rsplit("/", 1)[-1] if value else value


@tool
@retry_aws_call()
def aws_ecs_list_clusters() -> str:
    """List all ECS cluster ARNs in the configured AWS region."""
    client = get_boto3_client("ecs")
    clusters = []
    paginator = client.get_paginator("list_clusters")

    for page in paginator.paginate():
        clusters.extend(page.get("clusterArns", []))

    return _to_json(clusters)


@tool
@retry_aws_call()
def aws_ecs_describe_clusters(cluster_names: Optional[list[str]] = None) -> str:
    """Describe ECS clusters, including status, running tasks, pending tasks, active services, and registered instances."""
    client = get_boto3_client("ecs")

    if not cluster_names:
        cluster_arns = json.loads(aws_ecs_list_clusters.invoke({}))
        cluster_names = cluster_arns[:10]

    response = client.describe_clusters(
        clusters=cluster_names,
        include=["STATISTICS", "TAGS"],
    )

    clusters = []
    for cluster in response.get("clusters", []):
        clusters.append({
            "clusterName": cluster.get("clusterName"),
            "clusterArn": cluster.get("clusterArn"),
            "status": cluster.get("status"),
            "runningTasksCount": cluster.get("runningTasksCount"),
            "pendingTasksCount": cluster.get("pendingTasksCount"),
            "activeServicesCount": cluster.get("activeServicesCount"),
            "registeredContainerInstancesCount": cluster.get("registeredContainerInstancesCount"),
            "statistics": cluster.get("statistics", []),
            "tags": cluster.get("tags", []),
        })

    return _to_json(clusters)


@tool
@retry_aws_call()
def aws_ecs_list_services(cluster_name: str, launch_type: Optional[str] = None) -> str:
    """List ECS services in a cluster. Optional launch_type can be EC2, FARGATE, or EXTERNAL."""
    client = get_boto3_client("ecs")
    kwargs = {"cluster": cluster_name}

    if launch_type:
        kwargs["launchType"] = launch_type

    services = []
    paginator = client.get_paginator("list_services")

    for page in paginator.paginate(**kwargs):
        services.extend(page.get("serviceArns", []))

    return _to_json(services)


@tool
@retry_aws_call()
def aws_ecs_describe_services(cluster_name: str, service_names: list[str]) -> str:
    """Describe ECS services, including desired/running counts, deployment state, task definition, and load balancers."""
    client = get_boto3_client("ecs")
    response = client.describe_services(
        cluster=cluster_name,
        services=service_names,
        include=["TAGS"],
    )

    services = []
    for service in response.get("services", []):
        services.append({
            "serviceName": service.get("serviceName"),
            "serviceArn": service.get("serviceArn"),
            "status": service.get("status"),
            "desiredCount": service.get("desiredCount"),
            "runningCount": service.get("runningCount"),
            "pendingCount": service.get("pendingCount"),
            "launchType": service.get("launchType"),
            "platformVersion": service.get("platformVersion"),
            "taskDefinition": service.get("taskDefinition"),
            "deployments": service.get("deployments", []),
            "loadBalancers": service.get("loadBalancers", []),
            "networkConfiguration": service.get("networkConfiguration", {}),
            "tags": service.get("tags", []),
        })

    failures = response.get("failures", [])
    return _to_json({"services": services, "failures": failures})


@tool
@retry_aws_call()
def aws_ecs_list_tasks(cluster_name: str, service_name: Optional[str] = None, desired_status: str = "RUNNING") -> str:
    """List ECS task ARNs in a cluster, optionally filtered by service name and desired status."""
    client = get_boto3_client("ecs")
    kwargs = {
        "cluster": cluster_name,
        "desiredStatus": desired_status,
    }

    if service_name:
        kwargs["serviceName"] = service_name

    tasks = []
    paginator = client.get_paginator("list_tasks")

    for page in paginator.paginate(**kwargs):
        tasks.extend(page.get("taskArns", []))

    return _to_json(tasks)


@tool
@retry_aws_call()
def aws_ecs_describe_tasks(cluster_name: str, task_arns: list[str]) -> str:
    """Describe ECS tasks, including task status, containers, image names, image digests, CPU, and memory."""
    client = get_boto3_client("ecs")
    response = client.describe_tasks(
        cluster=cluster_name,
        tasks=task_arns,
        include=["TAGS"],
    )

    tasks = []
    for task in response.get("tasks", []):
        containers = []
        for container in task.get("containers", []):
            containers.append({
                "name": container.get("name"),
                "image": container.get("image"),
                "imageDigest": container.get("imageDigest"),
                "runtimeId": container.get("runtimeId"),
                "lastStatus": container.get("lastStatus"),
                "healthStatus": container.get("healthStatus"),
                "networkInterfaces": container.get("networkInterfaces", []),
            })

        tasks.append({
            "taskArn": task.get("taskArn"),
            "taskId": _short_arn(task.get("taskArn")),
            "clusterArn": task.get("clusterArn"),
            "lastStatus": task.get("lastStatus"),
            "desiredStatus": task.get("desiredStatus"),
            "healthStatus": task.get("healthStatus"),
            "launchType": task.get("launchType"),
            "taskDefinitionArn": task.get("taskDefinitionArn"),
            "cpu": task.get("cpu"),
            "memory": task.get("memory"),
            "containers": containers,
            "startedAt": task.get("startedAt"),
            "createdAt": task.get("createdAt"),
            "tags": task.get("tags", []),
        })

    failures = response.get("failures", [])
    return _to_json({"tasks": tasks, "failures": failures})


@tool
@retry_aws_call()
def aws_ecs_list_task_definitions(family_prefix: Optional[str] = None, status: str = "ACTIVE", max_items: int = 20) -> str:
    """List ECS task definition ARNs, optionally filtered by family prefix."""
    client = get_boto3_client("ecs")
    kwargs = {
        "status": status,
        "sort": "DESC",
    }

    if family_prefix:
        kwargs["familyPrefix"] = family_prefix

    response = client.list_task_definitions(**kwargs)
    return _to_json(response.get("taskDefinitionArns", [])[:max_items])


@tool
@retry_aws_call()
def aws_ecs_describe_task_definition(task_definition: str) -> str:
    """Describe an ECS task definition, including container image names, CPU, memory, ports, and environment variable names."""
    client = get_boto3_client("ecs")
    response = client.describe_task_definition(
        taskDefinition=task_definition,
        include=["TAGS"],
    )
    task_def = response.get("taskDefinition", {})

    containers = []
    for container in task_def.get("containerDefinitions", []):
        containers.append({
            "name": container.get("name"),
            "image": container.get("image"),
            "cpu": container.get("cpu"),
            "memory": container.get("memory"),
            "memoryReservation": container.get("memoryReservation"),
            "essential": container.get("essential"),
            "portMappings": container.get("portMappings", []),
            "environmentNames": [item.get("name") for item in container.get("environment", [])],
            "secretsNames": [item.get("name") for item in container.get("secrets", [])],
            "logConfiguration": container.get("logConfiguration", {}),
        })

    result = {
        "taskDefinitionArn": task_def.get("taskDefinitionArn"),
        "family": task_def.get("family"),
        "revision": task_def.get("revision"),
        "status": task_def.get("status"),
        "networkMode": task_def.get("networkMode"),
        "requiresCompatibilities": task_def.get("requiresCompatibilities", []),
        "cpu": task_def.get("cpu"),
        "memory": task_def.get("memory"),
        "taskRoleArn": task_def.get("taskRoleArn"),
        "executionRoleArn": task_def.get("executionRoleArn"),
        "containerDefinitions": containers,
        "tags": response.get("tags", []),
    }

    return _to_json(result)


@tool
@retry_aws_call()
def aws_ecs_get_service_images(cluster_name: str, service_names: list[str]) -> str:
    """Get container image names and task definition IDs used by one or more ECS services."""
    client = get_boto3_client("ecs")
    services_response = client.describe_services(
        cluster=cluster_name,
        services=service_names,
    )

    service_images = []
    for service in services_response.get("services", []):
        task_definition_arn = service.get("taskDefinition")
        task_def = client.describe_task_definition(
            taskDefinition=task_definition_arn,
        ).get("taskDefinition", {})

        images = []
        for container in task_def.get("containerDefinitions", []):
            images.append({
                "containerName": container.get("name"),
                "image": container.get("image"),
            })

        service_images.append({
            "serviceName": service.get("serviceName"),
            "taskDefinitionArn": task_definition_arn,
            "taskDefinitionId": _short_arn(task_definition_arn),
            "images": images,
        })

    failures = services_response.get("failures", [])
    return _to_json({"services": service_images, "failures": failures})


@tool
@retry_aws_call()
def aws_ecs_list_container_instances(cluster_name: str) -> str:
    """List ECS container instance ARNs for an ECS cluster."""
    client = get_boto3_client("ecs")
    instances = []
    paginator = client.get_paginator("list_container_instances")

    for page in paginator.paginate(cluster=cluster_name):
        instances.extend(page.get("containerInstanceArns", []))

    return _to_json(instances)


@tool
@retry_aws_call()
def aws_ecs_describe_container_instances(cluster_name: str, container_instance_arns: list[str]) -> str:
    """Describe ECS container instances, including EC2 instance ID, status, running tasks, resources, and agent status."""
    client = get_boto3_client("ecs")
    response = client.describe_container_instances(
        cluster=cluster_name,
        containerInstances=container_instance_arns,
        include=["TAGS"],
    )

    instances = []
    for instance in response.get("containerInstances", []):
        instances.append({
            "containerInstanceArn": instance.get("containerInstanceArn"),
            "ec2InstanceId": instance.get("ec2InstanceId"),
            "status": instance.get("status"),
            "agentConnected": instance.get("agentConnected"),
            "runningTasksCount": instance.get("runningTasksCount"),
            "pendingTasksCount": instance.get("pendingTasksCount"),
            "registeredResources": instance.get("registeredResources", []),
            "remainingResources": instance.get("remainingResources", []),
            "versionInfo": instance.get("versionInfo", {}),
            "healthStatus": instance.get("healthStatus", {}),
            "tags": instance.get("tags", []),
        })

    failures = response.get("failures", [])
    return _to_json({"containerInstances": instances, "failures": failures})

import json
from typing import Optional

from langchain_core.tools import tool

from tools.base import get_boto3_client
from utils.retry import retry_aws_call


def _to_json(data) -> str:
    return json.dumps(data, default=str)


@tool
@retry_aws_call()
def aws_eks_list_clusters() -> str:
    """List all EKS cluster names in the configured AWS region."""
    client = get_boto3_client("eks")
    clusters = []
    paginator = client.get_paginator("list_clusters")

    for page in paginator.paginate():
        clusters.extend(page.get("clusters", []))

    return _to_json(clusters)


@tool
@retry_aws_call()
def aws_eks_describe_cluster(cluster_name: str) -> str:
    """Describe an EKS cluster, including status, version, endpoint, role ARN, VPC config, and health issues."""
    client = get_boto3_client("eks")
    cluster = client.describe_cluster(name=cluster_name).get("cluster", {})

    result = {
        "name": cluster.get("name"),
        "arn": cluster.get("arn"),
        "status": cluster.get("status"),
        "version": cluster.get("version"),
        "platformVersion": cluster.get("platformVersion"),
        "endpoint": cluster.get("endpoint"),
        "roleArn": cluster.get("roleArn"),
        "createdAt": cluster.get("createdAt"),
        "health": cluster.get("health", {}),
        "resourcesVpcConfig": cluster.get("resourcesVpcConfig", {}),
        "logging": cluster.get("logging", {}),
        "tags": cluster.get("tags", {}),
    }

    return _to_json(result)


@tool
@retry_aws_call()
def aws_eks_get_cluster_health(cluster_name: str) -> str:
    """Get the current EKS cluster state and health issues for a cluster."""
    client = get_boto3_client("eks")
    cluster = client.describe_cluster(name=cluster_name).get("cluster", {})

    result = {
        "name": cluster.get("name"),
        "status": cluster.get("status"),
        "version": cluster.get("version"),
        "health": cluster.get("health", {}),
    }

    return _to_json(result)


@tool
@retry_aws_call()
def aws_eks_list_nodegroups(cluster_name: str) -> str:
    """List all managed node groups for an EKS cluster."""
    client = get_boto3_client("eks")
    nodegroups = []
    paginator = client.get_paginator("list_nodegroups")

    for page in paginator.paginate(clusterName=cluster_name):
        nodegroups.extend(page.get("nodegroups", []))

    return _to_json(nodegroups)


@tool
@retry_aws_call()
def aws_eks_describe_nodegroup(cluster_name: str, nodegroup_name: str) -> str:
    """Describe an EKS managed node group, including status, capacity, instance types, AMI type, and health."""
    client = get_boto3_client("eks")
    nodegroup = client.describe_nodegroup(
        clusterName=cluster_name,
        nodegroupName=nodegroup_name,
    ).get("nodegroup", {})

    result = {
        "nodegroupName": nodegroup.get("nodegroupName"),
        "clusterName": nodegroup.get("clusterName"),
        "status": nodegroup.get("status"),
        "capacityType": nodegroup.get("capacityType"),
        "instanceTypes": nodegroup.get("instanceTypes", []),
        "amiType": nodegroup.get("amiType"),
        "nodeRole": nodegroup.get("nodeRole"),
        "scalingConfig": nodegroup.get("scalingConfig", {}),
        "diskSize": nodegroup.get("diskSize"),
        "subnets": nodegroup.get("subnets", []),
        "health": nodegroup.get("health", {}),
        "version": nodegroup.get("version"),
        "releaseVersion": nodegroup.get("releaseVersion"),
        "createdAt": nodegroup.get("createdAt"),
        "modifiedAt": nodegroup.get("modifiedAt"),
        "tags": nodegroup.get("tags", {}),
    }

    return _to_json(result)


@tool
@retry_aws_call()
def aws_eks_list_addons(cluster_name: str) -> str:
    """List installed EKS add-ons for a cluster."""
    client = get_boto3_client("eks")
    addons = []
    paginator = client.get_paginator("list_addons")

    for page in paginator.paginate(clusterName=cluster_name):
        addons.extend(page.get("addons", []))

    return _to_json(addons)


@tool
@retry_aws_call()
def aws_eks_describe_addon(cluster_name: str, addon_name: str) -> str:
    """Describe an EKS add-on, including version, status, health, and service account role."""
    client = get_boto3_client("eks")
    addon = client.describe_addon(
        clusterName=cluster_name,
        addonName=addon_name,
    ).get("addon", {})

    result = {
        "addonName": addon.get("addonName"),
        "clusterName": addon.get("clusterName"),
        "status": addon.get("status"),
        "addonVersion": addon.get("addonVersion"),
        "serviceAccountRoleArn": addon.get("serviceAccountRoleArn"),
        "health": addon.get("health", {}),
        "createdAt": addon.get("createdAt"),
        "modifiedAt": addon.get("modifiedAt"),
        "tags": addon.get("tags", {}),
    }

    return _to_json(result)


@tool
@retry_aws_call()
def aws_eks_list_fargate_profiles(cluster_name: str) -> str:
    """List Fargate profiles for an EKS cluster."""
    client = get_boto3_client("eks")
    profiles = []
    paginator = client.get_paginator("list_fargate_profiles")

    for page in paginator.paginate(clusterName=cluster_name):
        profiles.extend(page.get("fargateProfileNames", []))

    return _to_json(profiles)


@tool
@retry_aws_call()
def aws_eks_describe_fargate_profile(cluster_name: str, fargate_profile_name: str) -> str:
    """Describe an EKS Fargate profile, including status, selectors, subnets, and pod execution role."""
    client = get_boto3_client("eks")
    profile = client.describe_fargate_profile(
        clusterName=cluster_name,
        fargateProfileName=fargate_profile_name,
    ).get("fargateProfile", {})

    result = {
        "fargateProfileName": profile.get("fargateProfileName"),
        "clusterName": profile.get("clusterName"),
        "status": profile.get("status"),
        "podExecutionRoleArn": profile.get("podExecutionRoleArn"),
        "subnets": profile.get("subnets", []),
        "selectors": profile.get("selectors", []),
        "createdAt": profile.get("createdAt"),
        "tags": profile.get("tags", {}),
    }

    return _to_json(result)


@tool
@retry_aws_call()
def aws_eks_list_updates(cluster_name: str, nodegroup_name: Optional[str] = None, addon_name: Optional[str] = None) -> str:
    """List recent EKS updates for a cluster, node group, or add-on."""
    client = get_boto3_client("eks")
    kwargs = {"name": cluster_name}

    if nodegroup_name:
        kwargs["nodegroupName"] = nodegroup_name
    if addon_name:
        kwargs["addonName"] = addon_name

    response = client.list_updates(**kwargs)
    return _to_json(response.get("updateIds", []))

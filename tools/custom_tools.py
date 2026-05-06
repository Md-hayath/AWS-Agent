from tools.aws_s3 import (
    aws_list_buckets, aws_create_bucket, aws_delete_bucket,
    aws_list_objects, aws_get_object, aws_put_object, aws_delete_object
)
from tools.aws_ec2 import (
    aws_describe_instances, aws_run_instances, aws_stop_instances,
    aws_start_instances, aws_terminate_instances, aws_describe_images
)
from tools.aws_eks import (
    aws_eks_list_clusters, aws_eks_describe_cluster, aws_eks_get_cluster_health,
    aws_eks_list_nodegroups, aws_eks_describe_nodegroup,
    aws_eks_list_addons, aws_eks_describe_addon,
    aws_eks_list_fargate_profiles, aws_eks_describe_fargate_profile,
    aws_eks_list_updates
)
from tools.aws_ecs import (
    aws_ecs_list_clusters, aws_ecs_describe_clusters,
    aws_ecs_list_services, aws_ecs_describe_services,
    aws_ecs_list_tasks, aws_ecs_describe_tasks,
    aws_ecs_list_task_definitions, aws_ecs_describe_task_definition,
    aws_ecs_get_service_images,
    aws_ecs_list_container_instances, aws_ecs_describe_container_instances
)
from tools.aws_dynamoDB import (
    aws_create_table, aws_put_item, aws_get_item,
    aws_query, aws_scan, aws_delete_item
)
from tools.aws_cf import (
    aws_create_stack, aws_update_stack, aws_delete_stack, aws_describe_stacks
)
from tools.aws_iam_sts import (
    aws_list_users, aws_create_user, aws_delete_user, aws_attach_user_policy,
    aws_list_roles, aws_pass_role, aws_assume_role, aws_get_caller_identity
)
from tools.aws_misc import (
    aws_get_metric_data, aws_describe_alarms,
    aws_create_function, aws_invoke,
    aws_create_topic, aws_publish,
    aws_create_queue, aws_send_message,
    aws_list_foundation_models
)

# Combine all tools into a single list to be provided to the agent
all_aws_tools = [
    aws_list_buckets, aws_create_bucket, aws_delete_bucket,
    aws_list_objects, aws_get_object, aws_put_object, aws_delete_object,
    aws_describe_instances, aws_run_instances, aws_stop_instances,
    aws_start_instances, aws_terminate_instances, aws_describe_images,
    aws_eks_list_clusters, aws_eks_describe_cluster, aws_eks_get_cluster_health,
    aws_eks_list_nodegroups, aws_eks_describe_nodegroup,
    aws_eks_list_addons, aws_eks_describe_addon,
    aws_eks_list_fargate_profiles, aws_eks_describe_fargate_profile,
    aws_eks_list_updates,
    aws_ecs_list_clusters, aws_ecs_describe_clusters,
    aws_ecs_list_services, aws_ecs_describe_services,
    aws_ecs_list_tasks, aws_ecs_describe_tasks,
    aws_ecs_list_task_definitions, aws_ecs_describe_task_definition,
    aws_ecs_get_service_images,
    aws_ecs_list_container_instances, aws_ecs_describe_container_instances,
    aws_create_table, aws_put_item, aws_get_item,
    aws_query, aws_scan, aws_delete_item,
    aws_create_stack, aws_update_stack, aws_delete_stack, aws_describe_stacks,
    aws_list_users, aws_create_user, aws_delete_user, aws_attach_user_policy,
    aws_list_roles, aws_pass_role, aws_assume_role, aws_get_caller_identity,
    aws_get_metric_data, aws_describe_alarms,
    aws_create_function, aws_invoke,
    aws_create_topic, aws_publish,
    aws_create_queue, aws_send_message,
    aws_list_foundation_models
]

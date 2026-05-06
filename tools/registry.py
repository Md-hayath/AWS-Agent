from tools.aws_ec2 import (
    aws_describe_instances,
    aws_run_instances,
    aws_stop_instances,
    aws_start_instances,
    aws_terminate_instances,
    aws_describe_images
)

# import other services too
# from tools.s3 import aws_list_buckets, aws_create_bucket ...

ALL_TOOLS = [
    aws_describe_instances,
    aws_run_instances,
    aws_stop_instances,
    aws_start_instances,
    aws_terminate_instances,
    aws_describe_images,
]

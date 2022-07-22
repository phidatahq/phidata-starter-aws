from phidata.infra.aws.config import AwsConfig, AwsResourceGroup
from phidata.infra.aws.create.iam.role import create_glue_iam_role
from phidata.infra.aws.resource.s3.bucket import S3Bucket

from workspace.dev.settings import dev_env, dev_key, dev_tags

# -*- AWS resources

# Shared aws settings
# skip_delete = True means resources will not be deleted on `phi ws down`
# Used in production to prevent accidental deletes
aws_skip_delete: bool = False

# -*- S3 buckets
# S3 bucket for storing data
dev_data_s3_bucket = S3Bucket(
    name=f"{dev_key}-data",
    acl="private",
    skip_delete=aws_skip_delete,
)

# Iam Role for Glue crawlers
dev_glue_iam_role = create_glue_iam_role(
    name=f"{dev_key}-glue-crawler-role",
    s3_buckets=[dev_data_s3_bucket],
    skip_delete=aws_skip_delete,
)

# -*- Define dev aws resources using the AwsConfig
dev_aws_config = AwsConfig(
    env=dev_env,
    resources=AwsResourceGroup(
        iam_roles=[dev_glue_iam_role],
        s3_buckets=[dev_data_s3_bucket],
    ),
)

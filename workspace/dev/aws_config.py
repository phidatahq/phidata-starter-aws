from phidata.infra.aws.config import AwsConfig

from workspace.dev.settings import dev_env
from workspace.dev.aws_resources import dev_aws_resources


# -*- Define dev aws resources using the AwsConfig
dev_aws_config = AwsConfig(
    env=dev_env,
    enabled=False,
    resources=[dev_aws_resources],
)

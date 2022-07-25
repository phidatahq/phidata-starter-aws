from phidata.infra.aws.resource.acm.certificate import AcmCertificate
from phidata.infra.aws.resource.eks.cluster import EksCluster
from phidata.infra.aws.resource.eks.kubeconfig import EksKubeconfig
from phidata.infra.aws.resource.eks.node_group import EksNodeGroup
from phidata.infra.aws.resource.group import AwsResourceGroup
from phidata.infra.aws.resource.s3.bucket import S3Bucket
from phidata.infra.aws.resource.cloudformation.stack import CloudFormationStack

from workspace.settings import ws_dir_path
from workspace.prd.settings import (
    prd_key,
    prd_tags,
    prd_domain,
    prd_subnets,
    prd_security_groups,
    services_ng_label,
    workers_ng_label,
)

# -*- AWS resources

# Shared aws settings
# skip_delete = True means resources will not be deleted on `phi ws down --env prd`
# Used in production to prevent accidental deletes
aws_skip_delete: bool = False

# -*- S3 buckets
# S3 bucket for storing logs
prd_logs_s3_bucket = S3Bucket(
    name=f"{prd_key}-logs",
    acl="private",
    skip_delete=aws_skip_delete,
)

# S3 bucket for storing data
prd_data_s3_bucket = S3Bucket(
    name=f"{prd_key}-data",
    acl="private",
    skip_delete=aws_skip_delete,
)

# -*- VPC stack for EKS
prd_vpc_stack = CloudFormationStack(
    name=f"{prd_key}-vpc",
    template_url="https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml",
    tags=prd_tags,
    skip_delete=aws_skip_delete,
)

# -*- EKS cluster
prd_eks_cluster = EksCluster(
    name=f"{prd_key}-cluster",
    vpc_stack=prd_vpc_stack,
    # To use other subnets/security groups,
    # comment out `vpc_stack` above and use:
    # resources_vpc_config={
    #     "subnetIds": prd_subnets,
    #     "securityGroupIds": prd_security_groups,
    # },
    tags=prd_tags,
    skip_delete=aws_skip_delete,
    # Skip kubeconfig update because we generate a kubeconfig
    # using the EksKubeconfig resource
    update_kubeconfig=False,
)
prd_eks_kubeconfig = EksKubeconfig(
    eks_cluster=prd_eks_cluster,
    # uncomment this line to assume the "eks-admin.role" in the kubeconfig.
    # Used by users not in the aws-auth configmap
    # kubeconfig_role=eks_admin_role,
)

# -*- EKS cluster nodegroup for running core services
prd_services_eks_nodegroup = EksNodeGroup(
    name=f"{prd_key}-services-ng",
    eks_cluster=prd_eks_cluster,
    min_size=2,
    max_size=5,
    desired_size=2,
    disk_size=256,
    instance_types=["m5.xlarge"],
    labels=services_ng_label,
    tags=prd_tags,
    skip_delete=aws_skip_delete,
)

# -*- EKS cluster nodegroup for running worker services
prd_worker_eks_nodegroup = EksNodeGroup(
    name=f"{prd_key}-workers-ng",
    eks_cluster=prd_eks_cluster,
    min_size=1,
    max_size=5,
    desired_size=2,
    disk_size=256,
    instance_types=["m5.xlarge"],
    labels=workers_ng_label,
    tags=prd_tags,
    skip_delete=aws_skip_delete,
)

# -*- ACM certificate for aws-dp.com
prd_aws_dp_certificate = AcmCertificate(
    name=prd_domain,
    domain_name=prd_domain,
    subject_alternative_names=[f"*.{prd_domain}"],
    store_cert_summary=True,
    certificate_summary_file=ws_dir_path.joinpath("aws", "acm", prd_domain),
    skip_delete=aws_skip_delete,
)

prd_aws_resources = AwsResourceGroup(
    name=prd_key,
    acm_certificates=[prd_aws_dp_certificate],
    s3_buckets=[prd_logs_s3_bucket, prd_data_s3_bucket],
    cloudformation_stacks=[prd_vpc_stack],
    eks_cluster=prd_eks_cluster,
    eks_kubeconfig=prd_eks_kubeconfig,
    eks_nodegroups=[prd_services_eks_nodegroup, prd_worker_eks_nodegroup],
)

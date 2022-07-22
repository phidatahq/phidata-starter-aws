from phidata.infra.aws.resource.iam.role import IamRole
from phidata.infra.aws.resource.iam.policy import IamPolicy
from phidata.infra.aws.resource.group import AwsResourceGroup
from phidata.infra.aws.create.iam.eks_admin_role import (
    create_eks_admin_role,
    create_assume_eks_admin_role_policy,
)
from phidata.infra.k8s.create.crb.eks_admin_crb import create_eks_admin_crb
from phidata.infra.k8s.resource.rbac_authorization_k8s_io.v1.cluste_role_binding import (
    ClusterRoleBinding,
)
from phidata.infra.k8s.resource.group import K8sResourceGroup

# -*- Eks Admin Aws Resources

# IMPORTANT: Add the AWS Account ID
aws_account_id: str = ""

# Create an eks_admin role for the eks_admin group members to assume
eks_admin_role: IamRole = create_eks_admin_role(
    account_id=aws_account_id,
)

# Create a policy that needs to be attached to the eks_admin group
assume_eks_admin_role_policy: IamPolicy = create_assume_eks_admin_role_policy(
    account_id=aws_account_id,
    eks_admin_role=eks_admin_role,
)

eks_admin_aws_resources = AwsResourceGroup(
    name="eks-admin",
    # Enable this resource group when needed
    enabled=False,
    iam_roles=[eks_admin_role],
    iam_policies=[assume_eks_admin_role_policy],
)

# -*- Eks Admin K8s Resources

# The username used with eksctl create iamidentitymapping
eks_admin_role_username = "eks_admin_role"
eks_admin_crb: ClusterRoleBinding = create_eks_admin_crb(
    users=[eks_admin_role_username]
)

eks_admin_k8s_resources = K8sResourceGroup(
    name="eks-admin",
    # Enable this resource group when needed
    enabled=False,
    crb=[eks_admin_crb],
)

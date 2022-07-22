# EKS Access

This document describes how to access staging/production kubernetes resources.

### User Access

When an Amazon EKS cluster is created, the cluster creator's IAM is automatically granted
`system:masters` permissions in the cluster's role-based access control (RBAC) configuration.

To grant additional AWS users/roles the ability to interact with the cluster,
we need to add them to the `aws-auth` ConfigMap.

- To add a user as an EKS Admin the `aws-auth` ConfigMap:

```sh
eksctl create iamidentitymapping \
    --cluster {EKS_CLUSTER_NAME} \
    --region={AWS_REGION} \
    --arn arn:aws:iam::{ACCOUNT_ID}:user/{USER} \
    --group system:masters \
    --no-duplicate-arns
```

To check the existing `aws-auth` ConfigMap:

```sh
eksctl get iamidentitymapping \
    --cluster aws-dp-prd-cluster \
    --region=us-east-1
```

### Group Access

According to AWS documentation `aws-auth.yaml` doesn’t support IAM groups.

But group based access can be provided using the following workaround:

1. Create an IAM role: "eks-admin.role".

2. Create a policy: "eks-admin.policy" with permissions to manage EKS and attach it to the "eks-admin.role" role.

3. Create a policy: "assume-eks-admin-role.policy" with permissions assuming the "eks-admin.role" role.

4. Create a user group: "eks_admin" and attach the "assume-eks-admin-role.policy" & "eks-admin.policy" permissions to it.

5. Update the kubeconfig to assume the "eks-admin.role" arn when signing the token.

6. Add the "eks-admin.role" ARN to the mapRoles section of configmap/aws-auth using

```
eksctl create iamidentitymapping \
    --cluster {EKS_CLUSTER_NAME} \
    --region={AWS_REGION} \
    --arn arn:aws:iam::{ACCOUNT_ID}:role/eks-admin.role \
    --group system:masters \
    --username eks_admin_role
```

7. Validate `aws-auth` ConfigMap

```
eksctl get iamidentitymapping \
    --cluster aws-dp-prd-cluster \
    --region=us-east-1
```

8. Create a ClusterRoleBinding to bind the "eks-admin.role" to the cluster-admin ClusterRole

- Create ClusterRoleBinding using

```sh
phi ws up --env stg --config k8s --app eks-admin
```

- Check ClusterRoleBinding is created

```sh
kubectl get clusterrolebindings
```

10. Users part of the "eks_admin" group can now assume the "eks-admin.role"
    using `kubectl` or the UI to access kubernetes clusters & resources.

---

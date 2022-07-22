# Production data platform

This guide describes how to manage the production data platform running on AWS.

Production Services:

- Traefik Dashboard: https://traefik.domain.com
- Airflow Webserver: https://airflow.domain.com
- Superset Webserver: https://superset.domain.com
- Airflow Flower: https://flower.domain.com
- Whoami: https://whoami.domain.com

## Deploying the production platform

The [workspace/prd](../workspace/prd) directory contains the code for the production platform.

Use `phi ws <command> --env prd` to create/update/delete prd resources.

1. Activate a virtual env

```sh
source ~/.venvs/dpenv/bin/activate
```

2. Create & push production images

Set `PUSH_DOCKER_IMAGES=True` in the `.env` file and run:

```sh
phi ws up --env prd --config docker --type image
```

3. Deploy aws resources

```sh
phi ws up --env prd --config aws
```

3. Deploy k8s resources

```sh
phi ws up --env prd --config k8s
```

4. After the superset-init container has completed its run, turn it down using:

```sh
phi ws down --env prd --config k8s --app superset-init
```

### Point `*.domain.com` to traefik loadbalancer

1. Find the loadbalancer external-ip for service `traefik-svc` using: `kubectl get svc`
2. Go to the `domain.com` hosted zone in route 53.
3. Create an A type record for `*.domain.com` and point to the external-ip of the network loadbalancer.

### Deploy the k8s dashboard

The k8s dashboard has 3 parts:

1. Metrics Server for collecting CPU/Mem metrics
2. Kubernetes Dashboard
3. EKS Admin Service Account for accessing the Kubernetes Dashboard

```sh
# Create the resources
kubectl apply -f workspace/k8s/dashboard

# check the deployment metrics-server
kubectl get deployment metrics-server -n kube-system

# check the service kubernetes-dashboard
kubectl get svc kubernetes-dashboard -n kubernetes-dashboard

# describe the service kubernetes-dashboard
kubectl describe svc kubernetes-dashboard -n kubernetes-dashboard
```

#### Access the k8s dashboard

Step 1: Retrieve an authentication token for the eks-admin service account.
Copy the <authentication_token> value from the output.
You use this token to connect to the dashboard.

```sh
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep eks-admin | awk '{print $1}')
```

Step 2: In another terminal start the kubectl proxy

```sh
kubectl proxy
```

Step 3: To access the dashboard endpoint, open the following [link](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#!/login.) with a web browser

http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#!/login

Step 4: Sign in using Token auth by pasting the <authentication_token> output from the previous command
into the Token field

#### Installing prometheus

```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prom-1 prometheus-community/prometheus
```

## Using the production environment

### Update kubeconfig

- Update kubeconfig using phidata:

```sh
phi ws up --env prd --config aws --name kubeconfig
```

- Update kubeconfig using aws:

```sh
aws eks update-kubeconfig \
  --name dp-prd-cluster \
  --region us-east-1
```

### View resources

```sh
k get all

k get deploy

k get nodes
```

## Create a production release

Please read the [production_release](./production_release.md) guide.

## Helpful commands

### How to create k8s dashboard admin user

1. Read [details here](https://docs.aws.amazon.com/eks/latest/userguide/dashboard-tutorial.html)
2. Create admin user using: `kubectl apply -f workspace/k8s/k8s-dashboard/eks-admin-service-account.yaml`

### How to connect to k8s dashboard using proxy

1. Get auth token using: `kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep eks-admin | awk '{print $1}')`
2. Start proxy: `kubectl proxy`
3. Access: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#!/login

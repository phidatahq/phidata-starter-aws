# Production release

This guide describes how to release aws-dp services to production

## Updating Airflow DAGs

Airflow picks up DAGs from the `production` branch,
which is released from the main branch using a git tag.

```sh
# Create a tag
git tag -a v0.1.7 -m "Version 0.1.7"

# Push tag to remote origin
git push origin v0.1.7

# Merge tag to production & release
git checkout production
git merge v0.1.7
git push origin production
```

## Update production images

After adding a new package/dependency, we should build & push new production images.

1. Please add the following to your `.env` to skip cache & do a hard pull of `FROM` images

```sh
PULL_DOCKER_IMAGES=True
PUSH_DOCKER_IMAGES=True
SKIP_DOCKER_CACHE=True
AIRFLOW_ENABLED=True
SUPERSET_ENABLED=True
```

2. Build + push prd images

```sh
CACHE=f phi ws up --env prd --config docker --type image -d
```

3. Confirm that new images are pushed to ECR

- [databox]()
- [airflow]()
- [superset]()

WARNING: If the client is not authenticated with ECR, we DO NOT get an error message and the **push to ECR fails silently**. Please authenticate with ECR first.

### Add new requirement/python package

To add a new package or dependency:

1. Add the module to the pyproject.toml file. [Example](https://github.com/Aws/data-platform/blob/main/pyproject.toml#L7)

2. Run: `./scripts/upgrade.sh`. This script updates the `requirements.txt` file.

3. Recreate images using either

```sh
phi ws patch --env prd --config docker --type image
```

OR

```sh
CACHE=f phi ws up --env prd --config docker --type image -d
```

## Update production services

After updating a config/env/secret, we need to do a rolling update of the corresponding services.

Do a rolling update of production deployments using:

```sh
# update databox deployments
phi ws patch --env prd --config k8s --app databox --type deployment

# update airflow deployments
phi ws patch --env prd --config k8s --name airflow --type deployment

# update superset deployments
phi ws patch --env prd --config k8s --name superset --type deployment
```

## Update Traefik Ingress

### Redeploy ingress after updating the routes

```sh
phi ws patch --env prd --name ingress --config k8s --type customobject
```

### Check ingressroute

```sh
k get ingressroutes
k describe ingressroutes websecure-ingress
```

### Recreate traefik app if needed

```sh
phi ws restart --env prd --config k8s --app traefik
```

### When we recreate the traefik-service, a new loadbalancer is created. How to point `*.aws-dp.com` to this new loadbalancer.

1. Go to the `aws-dp.com` hosted zone in route 53.
2. Find the loadbalancer external-ip for service `traefik-svc` using: `k get svc`
3. Click on the A type record for `*.aws-dp.com` and edit the record to point to the new loadbalancer.

---

### Optional: update airflow deployments by app

```sh
# airflow webserver
phi ws patch --env prd --config k8s --app airflow-ws --type deployment

# airflow scheduler
phi ws patch --env prd --config k8s --app airflow-scheduler --type
deployment

# airflow default worker
phi ws patch --env prd --config k8s --app airflow-default-worker --type deployment

# airflow high-pri worker
phi ws patch --env prd --config k8s --app airflow-high-pri-worker --type deployment
```

#### Patch all airflow resources

```sh
phi ws patch --env prd --config k8s --name airflow
```

#### Patch all airflow webserver resources

```sh
# update all resources for the airflow webserver
phi ws patch --env prd --config k8s --app airflow-ws
```

#### Patch app airflow scheduler resources

```sh
# update all resources for the airflow scheduler
phi ws patch --env prd --config k8s --app airflow-scheduler
```

## Example workflow:

- Make some change to production apps
- Run the following command to rolling restart airflow deployments
- Get pods using `k get pod`
- Check the logs to verify the update

```sh
phi ws patch --env prd --config k8s --name airflow --type deploy

# k get pod

kubectl logs -f --tail=2000 airflow-ws-deploy-8f5d5ddc5-dnvmp
```

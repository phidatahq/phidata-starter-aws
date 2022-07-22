# Production release

This guide describes how to release production services.

## Updating Airflow DAGs

When Git Sync is enabled, Airflow containers running in production pick up DAGs from the `main` branch. Merge to main and airflow should pick up the dags.

## Updating production images

After adding a new package/dependency, we should build & push new production images.

1. Please add the following to your `.env` to skip cache & do a hard pull of `FROM` images.

```sh
PULL_DOCKER_IMAGES=True
PUSH_DOCKER_IMAGES=True
SKIP_DOCKER_CACHE=True
...
```

2. Build + push prd images.

```sh
CACHE=f phi ws up --env prd --config docker --type image
```

3. Confirm that new images are pushed to your repo.

WARNING: When pushing images to ECR, the client may fail silently if not authenticated. Please validate & authenticate with ECR before pushing images.

4. Update production deployments to pick up new images (see commands below).

## Update production services

After creating a new image we need to do a rolling update of the corresponding deployments.

Do a rolling update of production deployments using:

```sh
# update airflow deployments
phi ws patch --env prd --config k8s --name airflow --type deployment

# update superset deployments
phi ws patch --env prd --config k8s --name superset --type deployment
```

After updating the configmap/env/secret, we need to patch all resources:

```sh
# update all airflow resources
phi ws patch --env prd --config k8s --app airflow

# update all superset resources
phi ws patch --env prd --config k8s --app superset
```

### Add new requirement/python package

To add a new package or dependency:

1. Add the module to the pyproject.toml file.

2. Run: `./scripts/upgrade.sh`. This script updates the `requirements.txt` file.

3. Recreate + push production images:

```sh
CACHE=f phi ws up --env prd --config docker --type image
```

4. Update production deployments:

```sh
# update airflow deployments
phi ws patch --env prd --config k8s --name airflow --type deployment
```

## Update Traefik Ingress

### Redeploy ingress after updating the routes

```sh
phi ws patch --env prd --config k8s --name ingress --type customobject
```

### Check ingressroute

```sh
kubectl get ingressroutes
kubectl describe ingressroutes websecure-ingress
```

### Recreate traefik app

```sh
phi ws restart --env prd --config k8s --app traefik
```

### Point `*.domain.com` to traefik loadbalancer

1. Find the loadbalancer external-ip for service `traefik-svc` using: `kubectl get svc`
2. Go to the `domain.com` hosted zone in route 53.
3. Edit the A type record for `*.domain.com` and point to the external-ip of the new network loadbalancer.

---

### Optional: update airflow deployments by app

```sh
# airflow webserver
phi ws patch --env prd --config k8s --app airflow-ws --type deployment

# airflow scheduler
phi ws patch --env prd --config k8s --app airflow-scheduler --type
deployment

# airflow worker
phi ws patch --env prd --config k8s --app airflow-worker --type deployment
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
- Get pods using `kubectl get pod`
- Check the logs to verify the update

```sh
phi ws patch --env prd --config k8s --name airflow --type deploy

# kubectl get pod

kubectl logs -f --tail=2000 airflow-ws-deploy-8f5d5ddc5-dnvmp
```

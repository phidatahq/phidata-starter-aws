# Debugging issues with the data platform

This guide describes how to debug issues with the data platform:

### Debug Airflow Webserver

Find webserver pod using `kubectl get pod`

1. Check logs

```sh
kubectl logs -f --tail=2000 airflow-ws-deploy-86cdbdd8cc-qtnwt -c airflow-ws-container

kubectl logs -f --tail=2000 airflow-ws-deploy-86cdbdd8cc-qtnwt -c git-sync-workspaces
```

2. Describe pod

```sh
k describe pod/airflow-ws-deploy-86cdbdd8cc-qtnwt
```

3. ssh into container & check workspaces

```sh
kubectl exec -it airflow-ws-deploy-86cdbdd8cc-qtnwt -c airflow-ws-container -- zsh

cd /mnt/workspaces
ls -l
```

### Debug Traefik

```sh
kubectl get ingressroutes
kubectl describe ingressroutes websecure-ingress
```

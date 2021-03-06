# Common Issues

This guide describes common issues and how to fix them.

## Development environment

### Databox airflow webserver unavailable

If the databox airflow webserver is unavailable at `http://databox.dp` or `http://localhost:8330/`.
Check the logs in the docker desktop or using `docker logs -f databox-dp-container`

If you notice the error: `The webserver is already running under PID 56.`

1. Delete the file `databox_airflow_home/airflow-webserver.pid`
2. Restart the databox

```sh
phi ws restart --name databox-dp-container
```

### Restart the airflow scheduler container

```sh
phi ws restart --name airflow-scheduler
```

### Check if db is accessible from a service

```sh
# get pod
kubectl get pod

# ssh into pod
kubectl exec -it databox-deploy-69f8f8dd95-wksdk -- zsh

# ping database
pg_isready \
	--dbname= \
	--host= \
	--port=5432 \
	--username=
```

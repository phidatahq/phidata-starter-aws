# Common Issues

This guide describes common issues and how to fix them.

## Development environment

### Databox airflow webserver unavailable

If the databox airflow webserver is unavailable at `http://databox.dp` or `http://localhost:8305/`.
Check the logs in the docker desktop or using `docker logs -f databox-container`

If you notice the error: `The webserver is already running under PID 56.`

1. Delete the file `databox_airflow_home/airflow-webserver.pid`
2. Restart the databox

```sh
phi ws restart --name databox-container
```

### Restart the airflow scheduler container

```sh
phi ws restart --name airflow-scheduler
```

### Run the scheduler in your databox

Open another terminal and run:

```sh
phi dx run "airflow scheduler"
```

### Check if db is accessible from a service

```sh
# get pod
kubectl get pod

# ssh into pod
kubectl exec -it databox-deploy-69f8f8dd95-wksdk -- zsh

# ping database
# core2
pg_isready \
	--dbname= \
	--host= \
	--port=5432 \
	--username=
# core3
pg_isready \
	--dbname= \
	--host= \
	--port=5432 \
	--username=
```

### Db not accessible from pod

If the rds cluster is not accessible from a pod, we need to add the EKS cluster security group to the inbound groups of the RDS cluster.

1. Find the security group for the RDS cluster.
2. Find the security group for the EKS cluster.
3. Add the EKS cluster sg to the inbound groups of the RDS cluster sg.

---

### Issue Heading

Issue Description

```sh
## fixes
```

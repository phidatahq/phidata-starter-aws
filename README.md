## AWS Data Platform

This repo contains the code for building a data platform on AWS.

We enable 2 data environments:

1. dev: A development env running on docker
2. prd: A production env running on aws + k8s

In this doc, we cover the setup + development environment. Additional docs to reference:

- The [Production](docs/production.md) guide covers the production data platform.
- The [Production Release](docs/production_release.md) doc covers how to release production services.
- The [Common Issues](docs/common_issues.md) doc covers common issues.

## Setup

1. Create + activate a virtual env:

```sh
python3 -m venv ~/.venvs/dpenv
source ~/.venvs/dpenv/bin/activate
```

2. Install + init `phidata`

```sh
pip install phidata
phi init
```

> from the `data-platform` dir:

3. Setup workspace:

```sh
phi ws setup
```

4. Copy `workspace/example_secrets` to `workspace/secrets`.

```sh
cp -r workspace/example_secrets workspace/secrets
```

Update the secrets in following files:

- [dev_databox_secrets.yml](workspace/secrets/dev_databox_secrets.yml)

5. Deploy the dev containers using:

```sh
phi ws up --env dev --config docker
```

`phi` will create the following resources:

- Image: `local/databox-dp:dev`
- Network: `dp`
- Container: `pg-db-dp-container`
- Container: `databox-dp-container`
- Container: `traefik-dp`

If the image build fails, try running again with debug logs:

```sh
phi ws up --env dev -d
```

Alternatively, you can also use a script to build each image:

```sh
./workspace/dev/images/build_databox_image.sh
./workspace/dev/images/build_airflow_image.sh
...
```

## Using the dev environment

The [workspace/dev](workspace/dev) directory contains the files defining the dev resources.

The `.env` file can be used to add environment variables, which in turn are used to enable/disable the following applications:

1. Databox App: for testing dags & pipelines (runs 1 container)
2. Airflow App: for running dags & pipelines (runs 5 containers)
3. Postgres App: for storing dev data (runs 1 container)
4. Superset App: for visualizing dev data (runs 4 containers)
5. Jupyter App: for analyzing dev data (runs 1 container)
6. Traefik App: a reverse proxy for routing `databox.dp` to the airflow webserver in the databox container

Apps are enabled using the following env vars in the `.env` file. The defaults are:

```sh
PG_DBS_ENABLED=True
DATABOX_ENABLED=True
AIRFLOW_ENABLED=False
SUPERSET_ENABLED=False
JUPYTER_ENABLED=False
TRAEFIK_ENABLED=True
```

Update the `.env` file and run:

```sh
phi ws up
```

> NOTE: The `phi ws ...` commands use the dev environment by default, so we can skip the `--env dev` flag.

### Airflow webserver in databox

Check out the airflow webserver running in the `databox-dp-container`:

- url: `http://localhost:8330/`
- user: `admin`
- pass: `admin`

**Optional:** Serve the databox airflow webserver at `http://databox.dp`

By running traefik locally, we can use local domains for our apps

1. Update the `/etc/hosts` file using: `sudo vim /etc/hosts`
2. Add the following lines at the end:

```sh
127.0.0.1 traefik.dp
127.0.0.1 airflow.dp
127.0.0.1 databox.dp
127.0.0.1 superset.dp
127.0.0.1 jupyter.dp
```

Open: http://databox.dp
Open: http://traefik.dp

### Format + lint workspace

Format with `black` & lint with `mypy` using:

```sh
./scripts/format.sh
```

If you need to install packages, run:

```sh
pip install black mypy
```

### Upgrading phidata version

> activate virtualenv: `source ~/.venvs/dpenv/bin/activate`

1. Upgrade phidata:

```sh
pip install phidata --upgrade
```

2. Rebuild local images & recreate containers:

```sh
CACHE=f phi ws up --env dev
```

### Optional: Install workspace locally

Install the workspace & python packages locally in your virtual env using:

```sh
./scripts/install.sh
```

This will:

1. Install python packages from `requirements.txt`
2. Install the data-platform package in `--editable` mode
3. Install `requirements-airflow.txt` without dependencies for code completion [_need to uncomment this step in script_]

This enables:

1. Running `black` & `mypy` locally
2. Running workflows locally
3. Editor auto-completion.

### Add python packages

Following [PEP-631](https://peps.python.org/pep-0631/), we should add dependencies to the [pyproject.toml](pyproject.toml) file.

To add a new package:

1. Add the module to the [pyproject.toml](/pyproject.toml) file.
2. Run: `./scripts/upgrade.sh`. This script updates the `requirements.txt` file.
3. _Optional: Run: `./scripts/install.sh` to install the new dependencies in a local virtual env._
4. Run `CACHE=false phi ws restart` to recreate images + containers

### Adding airflow providers

Airflow requirements are stored in the [workspace/dev/airflow_resources/requirements-airflow.txt](/workspace/dev//airflow_resources/requirements-airflow.txt) file.

To add new airflow providers:

1. Add the module to the [workspace/dev/airflow_resources/requirements-airflow.txt](/workspace/dev/airflow_resources/requirements-airflow.txt) file.
2. _Optional: Run: `./scripts/install.sh` to install the new dependencies in a local virtual env._
3. Run `CACHE=false phi ws restart` to recreate images + containers

### To force recreate all images & containers, use the `CACHE` env variable

```sh
CACHE=false phi ws up --env dev
```

### Shut down workspace

```sh
phi ws down
```

### Restart all resources

```sh
phi ws restart
```

### Restart all containers

```sh
phi ws restart --type container
```

### Restart all databox resources

```sh
phi ws restart --name databox
```

### Restart traefik

```sh
phi ws restart --app traefik
```

### Restart all airflow resources

```sh
phi ws restart --name airflow
```

### Add environment/secret variables to your apps

The containers read env using the `env_file` and secrets using the `secrets_file` params.
These files are stored in the [workspace/env](workspace/env) or [workspace/secrets](workspace/secrets) directories.

#### Databox

To add env variables to your databox container:

1. Update the [workspace/env/dev_databox_env.yml](workspace/env/dev_databox_env.yml) file.
2. Restart the databox container using: `phi ws restart --name databox --type container`

To add secret variables to your databox containers:

1. Update the [workspace/secrets/dev_databox_secrets.yml](workspace/secrets/dev_databox_secrets.yml) file.
2. Restart the databox container using: `phi ws restart --name databox --type container`

#### Airflow

To add env variables to your airflow containers:

1. Update the [workspace/env/dev_airflow_env.yml](workspace/env/dev_airflow_env.yml) file.
2. Restart all airflow containers using: `phi ws restart --name airflow --type container`

To add secret variables to your airflow containers:

1. Update the [workspace/secrets/dev_airflow_secrets.yml](workspace/secrets/dev_airflow_secrets.yml) file.
2. Restart all airflow containers using: `phi ws restart --name airflow --type container`

### Test a DAG

```sh
# ssh into databox or airflow-ws
docker exec -it databox-container zsh
docker exec -it airflow-ws-container zsh

# Test run the DAGs using module name
python -m data.products.dag_folder.dag_file

# Test run the DAG file
python /mnt/workspaces/dp/data/products/dag_folder/dag_file.py

# List DAGs
airflow dags list

# List tasks in DAG
airflow tasks list \
  -S /mnt/workspaces/dp/data/products/dag_folder/dag_file.py \
  -t dag_name

# Test airflow task
airflow tasks test dag_name task_name 2022-07-01
```

### Recreate everything

Notes:

- Use `data-platform` as the working directory
- Deactivate existing venv using `deactivate` if needed

```sh
echo "*- Deleting venv"
rm -rf ~/.venvs/dpenv

echo "*- Deleting databox_airflow_home"
rm -rf databox_airflow_home

echo "*- Deleting af-db-dp-volume volume"
docker volume rm af-db-dp-volume

echo "*- Recreating venv"
python3 -m venv ~/.venvs/dpenv
source ~/.venvs/dpenv/bin/activate

echo "*- Install phi"
pip install phidata
phi init

echo "*- Setup + deploying workspace"
phi ws setup
CACHE=f phi ws up
```

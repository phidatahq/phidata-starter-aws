from phidata.app.airflow import (
    AirflowWebserver,
    AirflowScheduler,
    AirflowWorker,
)
from phidata.app.postgres import PostgresDb
from phidata.app.redis import Redis

from workspace.dev.images import dev_airflow_image
from workspace.dev.pg_dbs import dev_pg_db_airflow_connections
from workspace.settings import ws_name, ws_dir_path, use_cache, airflow_enabled

# -*- Airflow docker resources

# Airflow db: A postgres instance to use as the database for airflow
dev_airflow_db = PostgresDb(
    name=f"af-db-{ws_name}",
    enabled=airflow_enabled,
    db_user="airflow",
    db_password="airflow",
    db_schema="airflow",
    # Connect to this db on port 8320
    container_host_port=8320,
)

# Airflow redis: A redis instance to use as the celery backend for airflow
dev_airflow_redis = Redis(
    name=f"af-redis-{ws_name}",
    enabled=airflow_enabled,
    command=["redis-server", "--save", "60", "1"],
    container_host_port=8321,
)

# Airflow webserver
dev_airflow_ws = AirflowWebserver(
    enabled=airflow_enabled,
    image_name=dev_airflow_image.name,
    image_tag=dev_airflow_image.tag,
    db_app=dev_airflow_db,
    wait_for_db=True,
    redis_app=dev_airflow_redis,
    wait_for_redis=True,
    executor="CeleryExecutor",
    mount_workspace=True,
    # Read env variables from env/dev_airflow_env.yml
    env_file=ws_dir_path.joinpath("env/dev_airflow_env.yml"),
    # Read secrets from env/dev_airflow_secrets.yml
    secrets_file=ws_dir_path.joinpath("secrets/dev_airflow_secrets.yml"),
    # Access the airflow webserver on http://localhost:8310
    webserver_host_port=8310,
    # use_cache=False will recreate the container every time you run `phi ws up`
    # Use it like: `CACHE=false phi ws up`
    use_cache=use_cache,
    # Serve the airflow webserver on airflow.dp
    container_labels={
        "traefik.enable": "true",
        "traefik.http.routers.airflow-ws.entrypoints": "http",
        "traefik.http.routers.airflow-ws.rule": "Host(`airflow.dp`)",
        # point the traefik loadbalancer to the webserver_port on the container
        "traefik.http.services.airflow-ws.loadbalancer.server.port": "8080",
    },
    db_connections=dev_pg_db_airflow_connections,
)

# Airflow scheduler
dev_airflow_scheduler = AirflowScheduler(
    enabled=airflow_enabled,
    image_name=dev_airflow_image.name,
    image_tag=dev_airflow_image.tag,
    db_app=dev_airflow_db,
    wait_for_db=True,
    # Init airflow db on container start -- ok to run everytime
    init_airflow_db=True,
    # Upgrade the airflow db on container start -- ok to run everytime
    upgrade_airflow_db=True,
    redis_app=dev_airflow_redis,
    wait_for_redis=True,
    executor="CeleryExecutor",
    mount_workspace=True,
    # Create an airflow admin user with username: admin, pass: admin
    create_airflow_admin_user=True,
    env_file=ws_dir_path.joinpath("env/dev_airflow_env.yml"),
    secrets_file=ws_dir_path.joinpath("secrets/dev_airflow_secrets.yml"),
    use_cache=use_cache,
    db_connections=dev_pg_db_airflow_connections,
)

# Airflow worker serving the default & tier_1 queues
dev_airflow_default_workers = AirflowWorker(
    enabled=airflow_enabled,
    queue_name="default,tier_1",
    image_name=dev_airflow_image.name,
    image_tag=dev_airflow_image.tag,
    db_app=dev_airflow_db,
    wait_for_db=True,
    redis_app=dev_airflow_redis,
    wait_for_redis=True,
    executor="CeleryExecutor",
    mount_workspace=True,
    env_file=ws_dir_path.joinpath("env/dev_airflow_env.yml"),
    secrets_file=ws_dir_path.joinpath("secrets/dev_airflow_secrets.yml"),
    use_cache=use_cache,
    db_connections=dev_pg_db_airflow_connections,
)

dev_airflow_apps = (
    [
        dev_airflow_db,
        dev_airflow_redis,
        dev_airflow_ws,
        dev_airflow_scheduler,
        dev_airflow_default_workers,
    ]
    if airflow_enabled
    else []
)

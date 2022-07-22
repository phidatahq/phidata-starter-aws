from phidata.app.postgres import PostgresDb
from phidata.app.redis import Redis
from phidata.app.superset import (
    SupersetWebserver,
    SupersetInit,
    SupersetWorker,
    SupersetWorkerBeat,
)

from workspace.settings import ws_name, ws_dir_path, use_cache, superset_enabled

# -*- Superset docker resources

# Superset db: A postgres instance to use as the database for superset
dev_superset_db = PostgresDb(
    name=f"ss-db-{ws_name}",
    enabled=superset_enabled,
    db_user="superset",
    db_password="superset",
    db_schema="superset",
    # Connect to this db on port 8340
    container_host_port=8340,
)

# Superset redis: A redis instance to use as the celery backend for superset
dev_superset_redis = Redis(
    name=f"ss-redis-{ws_name}",
    enabled=superset_enabled,
    command=["redis-server", "--save", "60", "1", "--loglevel", "debug"],
    container_host_port=6449,
)

# Superset webserver
dev_superset_ws = SupersetWebserver(
    enabled=superset_enabled,
    db_app=dev_superset_db,
    wait_for_db=True,
    redis_app=dev_superset_redis,
    wait_for_redis=True,
    mount_resources=True,
    resources_dir="workspace/dev/superset_resources",
    # Read env variables from env/dev_superset_env.yml
    env_file=ws_dir_path.joinpath("env/dev_superset_env.yml"),
    # Read secrets from env/dev_superset_secrets.yml
    secrets_file=ws_dir_path.joinpath("secrets/dev_superset_secrets.yml"),
    # Access the superset webserver on http://localhost:8410
    app_host_port=8410,
    # use_cache=False will recreate the container every time you run `phi ws up`
    # Use it like: `CACHE=false phi ws up`
    use_cache=use_cache,
    # Serve the superset webserver on superset.dp
    container_labels={
        "traefik.enable": "true",
        "traefik.http.routers.superset-ws.entrypoints": "http",
        "traefik.http.routers.superset-ws.rule": "Host(`superset.dp`)",
        # point the traefik loadbalancer to the app_port on the container
        "traefik.http.services.superset-ws.loadbalancer.server.port": "8088",
    },
)

# Superset init
# This container initializes for superset
# Only required once
dev_superset_init = SupersetInit(
    enabled=superset_enabled,
    db_app=dev_superset_db,
    wait_for_db=True,
    redis_app=dev_superset_redis,
    wait_for_redis=True,
    mount_resources=True,
    resources_dir="workspace/dev/superset_resources",
    # Read env variables from env/dev_superset_env.yml
    env_file=ws_dir_path.joinpath("env/dev_superset_env.yml"),
    # Read secrets from env/dev_superset_secrets.yml
    secrets_file=ws_dir_path.joinpath("secrets/dev_superset_secrets.yml"),
    load_examples=True,
    use_cache=use_cache,
)

# Superset worker
dev_superset_worker = SupersetWorker(
    enabled=superset_enabled,
    db_app=dev_superset_db,
    wait_for_db=True,
    redis_app=dev_superset_redis,
    wait_for_redis=True,
    mount_resources=True,
    resources_dir="workspace/dev/superset_resources",
    # Read env variables from env/dev_superset_env.yml
    env_file=ws_dir_path.joinpath("env/dev_superset_env.yml"),
    # Read secrets from env/dev_superset_secrets.yml
    secrets_file=ws_dir_path.joinpath("secrets/dev_superset_secrets.yml"),
    use_cache=use_cache,
)

# Superset worker beat
dev_superset_worker_beat = SupersetWorkerBeat(
    enabled=superset_enabled,
    db_app=dev_superset_db,
    wait_for_db=True,
    redis_app=dev_superset_redis,
    wait_for_redis=True,
    mount_resources=True,
    resources_dir="workspace/dev/superset_resources",
    # Read env variables from env/dev_superset_env.yml
    env_file=ws_dir_path.joinpath("env/dev_superset_env.yml"),
    # Read secrets from env/dev_superset_secrets.yml
    secrets_file=ws_dir_path.joinpath("secrets/dev_superset_secrets.yml"),
    use_cache=use_cache,
)

dev_superset_apps = [
    dev_superset_db,
    dev_superset_redis,
    dev_superset_ws,
    dev_superset_init,
    # dev_superset_worker,
    # dev_superset_worker_beat,
]

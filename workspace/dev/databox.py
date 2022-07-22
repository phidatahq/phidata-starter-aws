from phidata.app.databox import Databox

from workspace.dev.images import dev_databox_image
from workspace.dev.pg_dbs import dev_pg_db_airflow_connections
from workspace.settings import ws_name, ws_dir_path, use_cache, databox_enabled

# -*- Databox docker resources

# Databox: A containerized environment to run dev workflows
dev_databox = Databox(
    name=f"databox-{ws_name}",
    enabled=databox_enabled,
    image_name=dev_databox_image.name,
    image_tag=dev_databox_image.tag,
    # init_airflow initializes airflow and airflow db on the databox
    init_airflow=True,
    # Upgrade the airflow db on container start -- ok to run everytime
    upgrade_airflow_db=True,
    # Starts a standalone airflow service in this databox
    start_airflow_standalone=True,
    # Access the airflow webserver on http://localhost:8330
    airflow_standalone_host_port=8330,
    # This will mount airflow home from the databox to workspace_root/databox_airflow_home
    mount_airflow_home=True,
    # Create an airflow admin user with username: admin, pass: admin
    create_airflow_admin_user=True,
    # Read env variables from env/dev_databox_env.yml
    env_file=ws_dir_path.joinpath("env/dev_databox_env.yml"),
    # Read secrets from env/dev_databox_secrets.yml
    secrets_file=ws_dir_path.joinpath("secrets/dev_databox_secrets.yml"),
    # use_cache=False will recreate the container every time you run `phi ws up`
    # Use the CACHE env var like: `CACHE=false phi ws up`
    use_cache=use_cache,
    # Serve the airflow webserver on databox.dp
    container_labels={
        "traefik.enable": "true",
        "traefik.http.routers.databox.entrypoints": "http",
        "traefik.http.routers.databox.rule": "Host(`databox.dp`)",
        "traefik.http.services.databox.loadbalancer.server.port": "8080",
    },
    db_connections=dev_pg_db_airflow_connections,
)

dev_databox_apps = [dev_databox] if databox_enabled else []

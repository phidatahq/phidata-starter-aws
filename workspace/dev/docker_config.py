from phidata.infra.docker.config import DockerConfig

from workspace.settings import ws_name
from workspace.dev.airflow import dev_airflow_apps
from workspace.dev.databox import dev_databox_apps
from workspace.dev.pg_dbs import dev_pg_db_apps
from workspace.dev.jupyter import dev_jupyter_apps
from workspace.dev.superset import dev_superset_apps
from workspace.dev.traefik import dev_traefik_resources
from workspace.dev.images import dev_images

# -*- Define dev docker resources using the DockerConfig
dev_docker_config = DockerConfig(
    env="dev",
    network=ws_name,
    apps=dev_pg_db_apps
    + dev_airflow_apps
    + dev_superset_apps
    + dev_jupyter_apps
    + dev_databox_apps,
    images=dev_images,
    resources=[dev_traefik_resources],
)

from os import getenv

from phidata.infra.docker.resource.image import DockerImage
from workspace.settings import (
    ws_name,
    use_cache,
    airflow_enabled,
    databox_enabled,
    superset_enabled,
    data_platform_dir_path,
)

# -*- Prd Docker images

prd_images = []
image_repo = "phidata"
image_tag = "prd"
# Shared image params. Set using the .env file
skip_docker_cache = getenv("SKIP_DOCKER_CACHE", False)
pull_docker_images = getenv("PULL_DOCKER_IMAGES", False)
push_docker_images = True # getenv("PUSH_DOCKER_IMAGES", False)

# Airflow image
prd_airflow_image = DockerImage(
    name=f"{image_repo}/airflow-{ws_name}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/prd/images/airflow.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    # use_cache=False will recreate the image every time you run `phi ws up`
    # eg: `CACHE=f phi ws up`
    use_cache=use_cache,
)

if airflow_enabled:
    prd_images.append(prd_airflow_image)

# Databox image
prd_databox_image = DockerImage(
    name=f"{image_repo}/databox-{ws_name}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/prd/images/databox.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    use_cache=use_cache,
)

if databox_enabled:
    prd_images.append(prd_databox_image)

# Superset image
prd_superset_image = DockerImage(
    name=f"{image_repo}/superset-{ws_name}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/prd/images/superset.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    use_cache=use_cache,
)

if superset_enabled:
    prd_images.append(prd_superset_image)

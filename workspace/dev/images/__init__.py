from os import getenv

from phidata.infra.docker.resource.image import DockerImage
from workspace.settings import (
    ws_name,
    use_cache,
    airflow_enabled,
    databox_enabled,
    jupyter_enabled,
    data_platform_dir_path,
)

# -*- Dev Docker images

dev_images = []
image_tag = "dev"
# Shared image params. Set using the .env file
image_repo = getenv("IMAGE_REPO", "local")
skip_docker_cache = getenv("SKIP_DOCKER_CACHE", False)
pull_docker_images = getenv("PULL_DOCKER_IMAGES", False)
push_docker_images = getenv("PUSH_DOCKER_IMAGES", False)

# Airflow image
dev_airflow_image = DockerImage(
    name=f"{image_repo}/airflow-{ws_name}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/dev/images/airflow.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    # use_cache=False will recreate the image every time you run `phi ws up`
    # eg: `CACHE=f phi ws up`
    use_cache=use_cache,
)

if airflow_enabled:
    dev_images.append(dev_airflow_image)

# Databox image
dev_databox_image = DockerImage(
    name=f"{image_repo}/databox-{ws_name}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/dev/images/databox.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    use_cache=use_cache,
)

if databox_enabled:
    dev_images.append(dev_databox_image)

# Jupyter image
dev_jupyter_image = DockerImage(
    name=f"{image_repo}/jupyter-{ws_name}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/dev/images/jupyter.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    use_cache=use_cache,
)

if jupyter_enabled:
    dev_images.append(dev_jupyter_image)

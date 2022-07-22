from phidata.app.jupyter import JupyterLab

from workspace.dev.images import dev_jupyter_image
from workspace.settings import ws_name, ws_dir_path, use_cache, jupyter_enabled

# -*- Jupyter docker resources

# JupyterLab: Run dev notebooks
dev_jupyter = JupyterLab(
    name=f"jupyter-{ws_name}",
    enabled=jupyter_enabled,
    image_name=dev_jupyter_image.name,
    image_tag=dev_jupyter_image.tag,
    mount_workspace=True,
    # mounted when creating the image
    jupyter_config_file="/jupyter_lab_config.yml",
    # Read env variables from env/dev_jupyter_env.yml
    env_file=ws_dir_path.joinpath("env/dev_jupyter_env.yml"),
    # Read secrets from env/dev_jupyter_secrets.yml
    secrets_file=ws_dir_path.joinpath("secrets/dev_jupyter_secrets.yml"),
    use_cache=use_cache,
    # Serve the notebook server on jupyter.dp
    container_labels={
        "traefik.enable": "true",
        "traefik.http.routers.jupyter.entrypoints": "http",
        "traefik.http.routers.jupyter.rule": "Host(`jupyter.dp`)",
        "traefik.http.services.jupyter.loadbalancer.server.port": "8888",
    },
)

dev_jupyter_apps = [dev_jupyter] if jupyter_enabled else []

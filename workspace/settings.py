from pathlib import Path

from phidata.utils.env_var import env_var_is_true

# -*- Workspace settings

# Workspace name
ws_name: str = "dp"
# Path to the workspace directory
ws_dir_path: Path = Path(__file__).parent.resolve()
# Path to the root i.e. data platform directory
data_platform_dir_path: Path = ws_dir_path.parent
# Workspace git repo url
ws_repo: str = "https://github.com/phidatahq/phidata-starter-aws.git"

# -*- AWS settings

# Availability Zone for EbsVolumes
aws_az: str = "us-east-1a"
aws_region: str = "us-east-1"

# -*- Shared config params

# When CACHE=True then phi will not recreate existing resources.
# Example: `CACHE=f phi ws up --env dev --name databox --type container`
#           will restart existing databox container.
use_cache: bool = env_var_is_true("CACHE", True)

# -*- Enable apps using enviroment variables. Set in the .env file.

airflow_enabled: bool = env_var_is_true("AIRFLOW_ENABLED", False)
databox_enabled: bool = env_var_is_true("DATABOX_ENABLED", True)
jupyter_enabled: bool = env_var_is_true("JUPYTER_ENABLED", False)
pg_dbs_enabled: bool = env_var_is_true("PG_DBS_ENABLED", True)
superset_enabled: bool = env_var_is_true("SUPERSET_ENABLED", False)
traefik_enabled: bool = env_var_is_true("TRAEFIK_ENABLED", True)
whoami_enabled: bool = env_var_is_true("WHOAMI_ENABLED", True)

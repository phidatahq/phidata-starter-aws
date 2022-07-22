from os import getenv
from pathlib import Path

# -*- Workspace settings

# Workspace name
ws_name: str = "dp"
# Path to the workspace directory
ws_dir_path: Path = Path(__file__).parent.resolve()
# Path to the root i.e. data platform directory
data_platform_dir_path: Path = ws_dir_path.parent
# Workspace git repo url
ws_repo: str = "https://github.com/phidatahq/phidata-starter-basic.git"

# -*- AWS settings

# Availability Zone for EbsVolumes
aws_az: str = "us-east-1a"
aws_region: str = "us-east-1"

# -*- Shared config params

# When CACHE=True then phi will not recreate existing resources.
# Example: `CACHE=f phi ws up --env dev --name databox --type container`
#           will restart existing databox container.
use_cache: bool = getenv("CACHE", "true").lower().startswith("true")

# -*- Enable apps using enviroment variables. Set in the .env file.

pg_dbs_enabled: bool = getenv("PG_DBS_ENABLED", "true").lower().startswith("true")
databox_enabled: bool = getenv("DATABOX_ENABLED", "true").lower().startswith("true")
airflow_enabled: bool = getenv("AIRFLOW_ENABLED", "false").lower().startswith("true")
superset_enabled: bool = getenv("SUPERSET_ENABLED", "false").lower().startswith("true")
jupyter_enabled: bool = getenv("JUPYTER_ENABLED", "false").lower().startswith("true")
traefik_enabled: bool = getenv("TRAEFIK_ENABLED", "true").lower().startswith("true")

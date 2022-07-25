from os import getenv

# -*- The AIRFLOW_ENV env variable holds the current runtime environment
# Expected values: `dev`, `stg` or `prd`
AIRFLOW_ENV: str = getenv("AIRFLOW_ENV", "dev")

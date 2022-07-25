from data.env import AIRFLOW_ENV

from workspace.dev.pg_dbs import dev_pg_db_connection_id
from workspace.prd.pg_dbs import prd_pg_db_connection_id


# -*- Airflow Connections -*-

PG_DB: str = "pg_db"
if AIRFLOW_ENV == "prd":
    PG_DB = prd_pg_db_connection_id
else:
    PG_DB = dev_pg_db_connection_id

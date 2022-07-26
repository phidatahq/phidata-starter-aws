from data.env import AIRFLOW_ENV

from workspace.dev.pg_dbs import dev_pg_db_connection_id
from workspace.prd.pg_dbs import prd_pg_db_connection_id


# -*- Postgres Connections -*-

PG_DB_CONN_ID: str = "pg_db"
if AIRFLOW_ENV == "prd":
    PG_DB_CONN_ID = prd_pg_db_connection_id
else:
    PG_DB_CONN_ID = dev_pg_db_connection_id

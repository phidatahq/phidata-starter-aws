from datetime import timedelta

from data.common.connections.aws import AWS_DEFAULT_CONN_ID
from workspace.settings import aws_region

# -*- Default DAG arguments -*-

default_emails = [
    "data@team.com",
]

default_dag_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": default_emails,
    "email_on_failure": False,
    "retries": 3,
    "retry_delay": timedelta(seconds=30),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=5),
    "sla": timedelta(hours=16),
    "queue": "default",
    "region_name": aws_region,
    "aws_conn_id": AWS_DEFAULT_CONN_ID,
}

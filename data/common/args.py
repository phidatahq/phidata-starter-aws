from datetime import timedelta

# -*- Default DAG arguments -*-

aws_region: str = "us-east-1"
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
    "region_name": "us-east-1",
    "aws_conn_id": "aws_default",
}

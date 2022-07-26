import logging
from datetime import datetime
from typing import Dict

from airflow.decorators import dag, task
from phidata.asset.table.sql.postgres import PostgresTable

from data.common.args import default_dag_args
from data.common.connections.pg_db import PG_DB_CONN_ID

logger = logging.getLogger(__name__)

# -*- This DAG loads hourly cryptocurrency prices to
# the crypto_prices table.

coins = [
    "bitcoin",
    "ethereum",
    "litecoin",
    "ripple",
    "tether",
]

crypto_prices_table = PostgresTable(
    name="crypto_prices",
    db_conn_id=PG_DB_CONN_ID,
)


@dag(
    dag_id="download_crypto_prices",
    default_args=default_dag_args,
    description="Download cryptocurrency prices",
    schedule_interval="@hourly",
    max_active_tasks=5,
    start_date=datetime(2022, 1, 1),
    catchup=False,
)
def download_crypto_prices():
    @task(task_id="download_to_db")
    def download_to_db(**context) -> Dict[str, Dict]:
        import pandas as pd
        import requests

        logger.info(f"context: {context}")
        logger.info("Downloading cryptocurrency prices")
        response: Dict[str, Dict] = requests.get(
            url="https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": ",".join(coins),
                "vs_currencies": "usd",
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true",
                "include_last_updated_at": "true",
            },
        ).json()
        logging.info(f"type response: {type(response)}")
        logging.info(response)

        logging.info("Converting response to dataframe")
        df = pd.DataFrame.from_dict(response)
        logging.info(f"type df: {type(df)}")
        logging.info(df.head())

        return response

    download_to_db()


dag = download_crypto_prices()

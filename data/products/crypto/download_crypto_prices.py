from datetime import datetime
from logging import getLogger
from typing import Dict, Optional

from airflow.decorators import dag, task
from phidata.asset.table.sql.postgres import PostgresTable

from data.common.args import default_dag_args
from data.common.connections.pg_db import PG_DB_CONN_ID
from data.common.s3_buckets import DATA_S3_BUCKET

logger = getLogger(__name__)

##############################################################################
# This file defines a workflow that loads hourly cryptocurrency price data to
# 1. Postgres table: `crypto_prices`
# 2. S3 bucket: `dp-dev-data/crypto/prices`
##############################################################################

# List of coins to get prices for
coins = [
    "bitcoin",
    "ethereum",
    "litecoin",
    "ripple",
    "tether",
]

# -*- Load prices to postgres table -*-

# Step 1: Define a postgres table for storing crypto price data
crypto_prices_table = PostgresTable(
    name="crypto_prices",
    db_conn_id=PG_DB_CONN_ID,
)

# Step 2: Define tasks to load the postgres table
# 2.1 Drop existing price data
@task
def drop_existing_data(logical_date: Optional[datetime] = None) -> bool:
    """
    This task deletes data for a given (ds + hour) so we dont have duplicates
    """
    _dttm: datetime = logical_date or datetime.now()
    run_date = _dttm.strftime("%Y-%m-%d")
    run_hour = _dttm.strftime("%H")
    logger.info(f"Run date: {run_date}")
    logger.info(f"Run hour: {run_hour}")

    crypto_prices_table.run_sql_query(
        f"DELETE FROM {crypto_prices_table.name} WHERE ds = '{run_date}'"
    )
    return True


# 2.2 Load new price data
@task(task_id="write_to_db")
def write_to_db(logical_date: Optional[datetime] = None) -> bool:
    """
    Downloads cryptocurrency prices and load to postgres table.
    """

    import pandas as pd
    import requests

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

    _dttm: datetime = logical_date or datetime.now()
    run_date = _dttm.strftime("%Y-%m-%d")
    run_hour = _dttm.strftime("%H")
    logger.info(f"Run date: {run_date}")
    logger.info(f"Run hour: {run_hour}")

    logger.info("Converting response to dataframe")
    _df = pd.DataFrame.from_dict(response, orient="index")
    _df["ds"] = run_date
    _df["hour"] = run_hour
    print(_df.head())

    return True


# -*- Load prices to S3 dataset -*-

load_to_s3 = True


@task(task_id="write_to_s3")
def write_to_s3(logical_date: Optional[datetime] = None) -> bool:
    _dttm: datetime = logical_date or datetime.now()
    logger.info(f"Datetime: {_dttm}")

    return True


# -*- Define DAG -*-
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

    load_pg_db = write_to_db(drop_existing_data())

    if load_to_s3:
        load_s3 = write_to_s3(load_pg_db)


dag = download_crypto_prices()

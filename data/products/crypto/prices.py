from typing import Dict

from phidata.asset.table.sql.postgres import PostgresTable
from phidata.workflow import Workflow
from phidata.task import TaskArgs, task
from phidata.utils.log import logger

from data.common.args import default_dag_args
from data.common.connections.pg_db import PG_DB_CONN_ID
from workspace.dev.pg_dbs import dev_pg_db

##############################################################################
# This file defines a workflow that loads hourly cryptocurrency price data to
# a postgres table: `crypto_prices`
##############################################################################

# List of coins to get prices for
coins = [
    "bitcoin",
    "ethereum",
    "litecoin",
    "ripple",
    "tether",
]

# Step 1: Define a postgres table for storing crypto price data
crypto_prices_table = PostgresTable(
    name="crypto_prices",
    db_conn_id=PG_DB_CONN_ID,
    db_conn_url=dev_pg_db.get_db_connection_url_local(),
)

# Step 2: Build a workflow that loads the crypto_prices_table

# 2.1 Drop existing price data
@task
def drop_existing_data(**kwargs) -> bool:
    """
    Drop rows for current window (ds + hour) to prevent duplicates
    """
    args: TaskArgs = TaskArgs.from_kwargs(kwargs)
    run_date = args.run_date
    run_day = run_date.strftime("%Y-%m-%d")
    run_hour = run_date.strftime("%H")

    logger.info(f"Dropping rows for: ds={run_day}/hr={run_hour}")
    try:
        crypto_prices_table.run_sql_query(
            f"""
            DELETE FROM {crypto_prices_table.name}
            WHERE
                ds = '{run_day}'
                AND hour = '{run_hour}'
            """
        )
    except Exception as e:
        logger.error(f"Error dropping rows: {e}")
    return True


# 2.2 Load new price data
@task
def write_to_db(**kwargs) -> bool:
    """
    Download prices and load postgres table.
    """
    import pandas as pd
    import requests

    args: TaskArgs = TaskArgs.from_kwargs(kwargs)
    run_date = args.run_date
    run_day = run_date.strftime("%Y-%m-%d")
    run_hour = run_date.strftime("%H")

    logger.info(f"Downloading prices for: ds={run_day}/hr={run_hour}")
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

    logger.info("Converting response to dataframe")
    _df = pd.DataFrame.from_dict(response, orient="index")
    _df.index.name = "ticker"
    _df["ds"] = run_day
    _df["hour"] = run_hour
    _df.reset_index(inplace=True)
    _df.set_index(["ds", "hour", "ticker"], inplace=True)

    print(_df.head())

    return crypto_prices_table.write_pandas_df(_df, if_exists="append")


# 2.3: Instantiate tasks
drop = drop_existing_data(enabled=False)
load_prices = write_to_db()

# 2.4: Create a Workflow and add the tasks
crypto_prices = Workflow(
    name="crypto_prices",
    tasks=[drop, load_prices],
    graph={
        load_prices: [drop],
    },
    outputs=[crypto_prices_table],
)

# 2.5: Create a DAG for the workflow
dag = crypto_prices.create_airflow_dag(is_paused_upon_creation=True)

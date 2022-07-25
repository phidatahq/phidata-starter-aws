from phidata.asset.aws.s3 import S3Object
from phidata.asset.aws.athena.query import AthenaQuery
from phidata.task.aws.athena import RunAthenaQuery
from phidata.task.aws.glue import StartGlueCrawler
from phidata.task.download.url.to_s3 import DownloadUrlToS3
from phidata.infra.aws.resource.glue.crawler import GlueCrawler, GlueS3Target
from phidata.workflow import Workflow

from workspace.dev.aws_config import dev_data_s3_bucket, dev_glue_iam_role

##############################################################################
## An example data pipeline that calculates daily user count using s3, athena and glue.
## Steps:
##  1. Download user_activity data from a URL and upload to s3.
##  2. Create a glue crawler which creates a table from the file.
##  3. Run an athena query to calculate daily user count.
##############################################################################

# Step 1: Download user_activity data from a URL and upload to s3.
# Define a S3 object for this file. Use the dev_data_s3_bucket from the workspace config.
table_name = "daily_active_users"
user_activity_s3 = S3Object(
    key=f"{table_name}/ds_2021_10_01.csv",
    bucket=dev_data_s3_bucket,
)

# Create a task that downloads the file and uploads to s3
url = "https://raw.githubusercontent.com/phidatahq/demo-data/main/dau_2021_10_01.csv"
download = DownloadUrlToS3(
    name="download",
    url=url,
    s3_object=user_activity_s3,
)

# Step 2: Create a glue crawler which creates a table from the file.
# Define a GlueCrawler for the S3 object. Use the dev_glue_iam_role from the workspace config.
database_name = "users"
user_activity_crawler = GlueCrawler(
    name=f"{table_name}_crawler",
    iam_role=dev_glue_iam_role,
    database_name=database_name,
    s3_targets=[
        GlueS3Target(
            dir=table_name,
            bucket=dev_data_s3_bucket,
        )
    ],
)

# Create a task that creates and starts the crawler
start_crawler = StartGlueCrawler(
    name="start_crawler",
    crawler=user_activity_crawler,
)

# Step 3: Run an athena query to calculate daily user count.
query = RunAthenaQuery(
    name="query",
    query=AthenaQuery(
        name="dau_query",
        query_string=f"""
        SELECT
            ds,
            SUM(CASE WHEN is_active=1 THEN 1 ELSE 0 END) AS active_users
        FROM {database_name}.{table_name}
        GROUP BY ds
        ORDER BY ds
        """,
        database=database_name,
        output_location=f"s3://{dev_data_s3_bucket.name}/queries/{database_name}/{table_name}/",
    ),
    get_results=True,
)

# Create a workflow for these tasks.
# We run the query task manually so do not add it as part of the workflow.
dau_aws = Workflow(
    name="dau_aws",
    tasks=[
        download,
        start_crawler,
    ],
)
dag = dau_aws.create_airflow_dag(is_paused_upon_creation=True)

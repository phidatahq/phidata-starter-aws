from data.env import AIRFLOW_ENV

from workspace.dev.aws_resources import dev_data_s3_bucket, dev_logs_s3_bucket
from workspace.prd.aws_resources import prd_data_s3_bucket, prd_logs_s3_bucket

# -*- S3 Buckets -*-

# The S3 bucket for storing data
DATA_S3_BUCKET: str
if AIRFLOW_ENV == "prd":
    DATA_S3_BUCKET = prd_data_s3_bucket.name
else:
    DATA_S3_BUCKET = dev_data_s3_bucket.name

# The S3 bucket for storing logs
LOGS_S3_BUCKET: str
if AIRFLOW_ENV == "prd":
    LOGS_S3_BUCKET = prd_logs_s3_bucket.name
else:
    LOGS_S3_BUCKET = dev_logs_s3_bucket.name

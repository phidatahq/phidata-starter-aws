This folder contains DAGs that are part of the `crypto` data product.

### Test DAGs

```sh
# ssh into airflow-ws or airflow-worker
docker exec -it airflow-worker-container zsh

# Test run the DAG file
python mnt/workspaces/phidata-starter-aws/data/products/crypto/download_crypto_prices.py

# List DAGs
airflow dags list

# List tasks in DAG
airflow tasks list -t download_crypto_prices

# Test airflow task
airflow tasks test \
  download_crypto_prices \
  download_to_db \
  2022-07-01
```
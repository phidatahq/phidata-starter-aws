This folder contains DAGs that are part of the `crypto` data product.

### Test DAGs

```sh
# ssh into airflow-ws or airflow-worker
docker exec -it airflow-worker-container zsh

# Test run the DAG file
python mnt/workspaces/phidata-starter-aws/data/products/crypto/prices.py

# List DAGs
airflow dags list

# List tasks
airflow tasks list -t crypto_prices

# Test tasks
airflow tasks test \
  crypto_prices \
  write_to_db \
  2022-07-01

airflow tasks test \
  crypto_prices \
  drop_existing_data \
  2022-07-01

# Test tasks for ds + hour
airflow tasks test \
  crypto_prices \
  write_to_db \
  2022-07-01T01:05:00
```

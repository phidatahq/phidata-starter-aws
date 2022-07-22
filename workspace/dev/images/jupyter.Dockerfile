FROM phidata/jupyterlab:3.4.3

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY workspace/dev/airflow_resources /
RUN pip install -r /requirements-airflow.txt

COPY workspace/dev/jupyter_resources /
RUN pip install -r /requirements-jupyter.txt

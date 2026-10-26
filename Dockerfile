FROM apache/airflow:2.11.2

WORKDIR /opt/airflow

COPY pyproject.toml ./
COPY src ./src
COPY README.md ./

RUN pip install --no-cache-dir \
    "apache-airflow==2.11.2" \
    apache-airflow-providers-clickhousedb \
    .
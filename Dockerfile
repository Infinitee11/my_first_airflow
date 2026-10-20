FROM apache/airflow:2.11.2
# Указываем, что провайдер должен быть установлен для Airflow 2.11.2
RUN pip install --no-cache-dir \
    "apache-airflow==2.11.2" \
    apache-airflow-providers-clickhousedb
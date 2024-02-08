FROM apache/airflow:2.8.1

USER root

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

USER airflow

RUN pip install apache-airflow==${AIRFLOW_VERSION} meltano==3.3.1

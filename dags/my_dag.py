from datetime import datetime
from random import randint

from airflow.providers.docker.operators.docker import DockerOperator
# from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

from airflow import DAG


default_args = { }


def meltano_task(task_id, pipeline_name):
    return DockerOperator(
        task_id=task_id,
        image='meltano:1.0',
        container_name='task__pipeline',
        api_version= 'auto',
        docker_url="unix://var/run/docker.sock",
        auto_remove=True,
        network_mode='bridge',
        entrypoint=[
            "bash",
            "-c",
            f"meltano run {pipeline_name}"
        ]
    )

with DAG(dag_id="lighthouse_challenge", default_args=default_args, start_date=datetime(2020, 1, 1), schedule_interval="@daily", catchup=False) as dag:

    with TaskGroup(group_id="extracts") as extract_tasks:

        extract_csv = meltano_task('csv', 'extract-csv')

        extract_postgres = meltano_task('postgres', 'extract-postgres')

        send_to_db = meltano_task('lighthouse', 'send-to-lighthouse')

extract_csv >> extract_postgres >> send_to_db


# Code snippet from the BashOperator try:
        #   hello_world = BashOperator(
        #        task_id= "teste",
        #        bash_command="cd /opt/airflow/meltano && pip install meltano && meltano install extractors && meltano install loaders && meltano run extract-csv"
        #   )
    
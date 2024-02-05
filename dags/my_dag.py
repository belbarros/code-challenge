from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

def extract_csv():
    return 'meltano'

with DAG("lighthouse_challenge", start_date=datetime(2020, 1, 1), schedule_interval="@daily", catchup=False) as dag:
    extract_csv = PythonOperator(
        task_id='extract_csv',
        python_callable=extract_csv
    )

    extract_postgres = PythonOperator(
        task_id='extract_postgres',
        python_callable=''
    )

    # save_local = PythonOperator(
    #     task_id='save_local',
    #     python_callable=''
    # )

    save_db = PythonOperator(
        task_id='save_db',
        python_callable=''
    )

extract_csv >> save_db
extract_postgres >> save_db   
    

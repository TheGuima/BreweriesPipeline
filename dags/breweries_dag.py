import os
import json
from datetime import timedelta

import requests
import pandas as pd
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowFailException
from airflow.operators.python_operator import PythonOperator


# Create bronze layer
def fetch_data():
    try:
        response = requests.get("https://api.openbrewerydb.org/breweries")
        data = response.json()

        #  Save raw data
        os.makedirs("/opt/airflow/data/bronze", exist_ok=True) 
        with open('/opt/airflow/data/bronze/data.json', 'w') as f:
            json.dump(data, f)

    except Exception as e:
        raise AirflowFailException(f"Data fetching failed: {e}")

# Create silver layer
def transform_data_to_parquet():
    df = pd.read_json('/opt/airflow/data/bronze/data.json')
    os.makedirs("/opt/airflow/data/silver", exist_ok=True) 
    df.to_parquet('/opt/airflow/data/silver/data.parquet')
    
# Create gold layer 
def aggregate_data():
    df = pd.read_parquet('/opt/airflow/data/silver/data.parquet')
    # The test says to aggregate by location, so Iḿ creating a view based on city and another based on state
    aggregated_df_city = df.groupby(['brewery_type', 'city']).size().reset_index(name='count')
    aggregated_df_state = df.groupby(['brewery_type', 'state']).size().reset_index(name='count')
    
    os.makedirs("/opt/airflow/data/gold", exist_ok=True) 
    aggregated_df_city.to_parquet('/opt/airflow/data/gold/view_by_type_and_city.parquet')
    aggregated_df_state.to_parquet('/opt/airflow/data/gold/view_by_type_and_state.parquet')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'breweries_pipeline',
    default_args=default_args,
    description='A pipeline to process breweries data and create views based on type and location',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
)

fetch_task = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data_to_parquet',
    python_callable=transform_data_to_parquet,
    dag=dag,
)

aggregate_task = PythonOperator(
    task_id='aggregate_data',
    python_callable=aggregate_data,
    dag=dag,
)

fetch_task >> transform_task >> aggregate_task

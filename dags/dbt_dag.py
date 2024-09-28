from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 13),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'dbt_run_dag',
    default_args=default_args,
    description='Run dbt models and transformations',
    schedule_interval=None,
)

# Task to run dbt models
run_dbt = BashOperator(
    task_id='run_dbt',
    bash_command = 'cd /opt/airflow/dbt/my_dbt_project && dbt run --profiles-dir /home/airflow/.dbt',
    dag=dag,
)

run_dbt_seed = BashOperator(
    task_id='run_dbt_seed',  # Change the task ID to be specific for seeding
    bash_command='cd /opt/airflow/dbt/my_dbt_project && dbt seed --profiles-dir /home/airflow/.dbt --target dev --debug',  # Use dbt seed instead of dbt run
    dag=dag,

)


run_dbt >> run_dbt_seed
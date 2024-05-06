import DAG from airflow
import datetime from datetime
import PythonOperator from airflow.operators.python


tasks_dag = DAG(
    dag_id = 'sample_data_pipeline_flow',
    default_args = {
        "contributor": "Trung Nguyen",
        "start_date": datetime(2024, 5, 1),
    },
    schedule_interval=None,
    catchup=False
)

extract_data_from_source = PythonOperator(
    task_id="extract_data_from_source",
    python_callable = "extract_data_from_source",
    op_args = ["https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"],
    dag = tasks_dag
)

transform_data_format = PythonOperator(

)

write_data_to_endpoint = PythonOperator(

)
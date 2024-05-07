import DAG from airflow
import sys
import datetime from datetime
import PythonOperator from airflow.operators.python

# make this module available for import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import extract_data_from_source_callable, transform_data_format_callable, write_data_to_sink_callable from pipelines.pipeline

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
    task_id = "extract_data_from_source",
    python_callable = extract_data_from_source_callable,
    provide_context=True,
    op_args = ["https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"],
    dag = tasks_dag
)

transform_data_format = PythonOperator(
    task_id = "transform_data_format",
    python_callable = transform_data_format_callable,
    provide_context=True,
    dag = tasks_dag
)

write_data_to_sink = PythonOperator(
    task_id = "write_data_to_sink",
    python_callable = write_data_to_sink_callable,
    provide_context=True,
    dag = tasks_dag
)

# flow define
extract_data_from_source >> transform_data_format >> write_data_to_sink
from airflow import DAG 
from datetime import datetime,timedelta
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator


def print_data(**context):
    fetched_data=context['ti'].xcom_pull(task_ids='fech_mysql_data')
    print(fetched_data)

default_args={'owner':'Akhil',
              'start_date':datetime(2023,7,7),
               'end_date':datetime(2023,8,1),
               'retry_delay':timedelta(minutes=5)}

dag=DAG('data_retrieval_operation',
        default_args=default_args,
        schedule='@daily')


fetch_data=SQLExecuteQueryOperator(
               task_id='fetch_mysql_data',
               conn_id='Mysql_Db_Fetch',
                sql='''Select o.orderid as Orderid, sum(o.netamount) as NetAmount
                                from orders as o
                                limit 10''',
                database='shoekonnect_live',
                        dag=dag)

print_data=PythonOperator(task_id='print_dataset',
                         python_callable=print_data,
                          dag=dag )

fetch_data >> print_data
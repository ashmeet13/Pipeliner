from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.slack.operators.slack_webhook import SlackWebhookHook
from airflow.utils.dates import days_ago

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {"owner": "admin"}

dag = DAG(
    dag_id="simple_etl",
    default_args=default_args,
    schedule_interval="*/5 * * * *",
    start_date=days_ago(0),
    tags=["etl"],
    max_active_runs=1,
    catchup=False,
)


def extract_total_sales(**kwargs):
    ti = kwargs.get("ti")
    source_db = PostgresHook(postgres_conn_id="postgres_online_store")
    source_connection = source_db.get_conn()
    cursor = source_connection.cursor()

    query = """SELECT SUM(item.item_price::numeric)
                FROM orders
                JOIN item ON orders.item_id = item.item_id
                WHERE orders.order_time>%s AND orders.order_time<=%s;"""

    cursor.execute(
        query, (kwargs.get("prev_execution_date"), kwargs.get("execution_date"))
    )
    data = cursor.fetchall()

    cursor.close()
    ti.xcom_push(key="total_order_sales", value=float(data[0][0]))


def extract_brand_wise_sales(**kwargs):
    ti = kwargs.get("ti")
    source_db = PostgresHook(postgres_conn_id="postgres_online_store")
    source_connection = source_db.get_conn()
    cursor = source_connection.cursor()

    query = """SELECT brand.brand_name, SUM(item.item_price::numeric)
                FROM orders
                JOIN item ON orders.item_id = item.item_id
                JOIN brand ON item.brand_id = brand.brand_id
                WHERE orders.order_time>%s AND orders.order_time<=%s
                GROUP BY brand.brand_name
                ORDER BY brand.brand_name;"""

    cursor.execute(
        query, (kwargs.get("prev_execution_date"), kwargs.get("execution_date"))
    )
    data = cursor.fetchall()

    formatted_data = []
    for brand_index in range(len(data)):
        formatted_data.append((data[brand_index][0], float(data[brand_index][1])))

    cursor.close()
    ti.xcom_push(key="brand_wise_sale", value=formatted_data)


def send_slack_message(**kwargs):
    ti = kwargs.get("ti")
    prev_execution_date, execution_date = (
        kwargs.get("prev_execution_date"),
        kwargs.get("execution_date"),
    )
    total_order_sales = ti.xcom_pull(
        key="total_order_sales", task_ids="extract_total_sales"
    )
    brand_wise_sale = ti.xcom_pull(
        key="brand_wise_sale", task_ids="extract_brand_wise_sales"
    )

    message = f"{prev_execution_date.tz}"
    message += "\n" + f"Start Time = {prev_execution_date.to_day_datetime_string()}"
    message += "\n" + f"End Time = {execution_date.to_day_datetime_string()}"

    message += "\n\n" + f"Total Sales of ${total_order_sales} made"

    temp_messages = []

    for brand_sale in brand_wise_sale:
        temp_messages.append(f"{brand_sale[0]} made a total sale of ${brand_sale[1]}")

    message += "\n\n" + "\n".join(temp_messages)

    slack_hook = SlackWebhookHook(
        http_conn_id="slack_connection",
        message=message,
        webhook_token=BaseHook.get_connection("slack_connection").password,
        username="admin",
    )
    slack_hook.execute()


extract_total_sales_task = PythonOperator(
    task_id="extract_total_sales", python_callable=extract_total_sales, dag=dag
)

extract_brand_wise_sales_task = PythonOperator(
    task_id="extract_brand_wise_sales",
    python_callable=extract_brand_wise_sales,
    dag=dag,
)

slack_task = PythonOperator(
    task_id="send_slack_message", python_callable=send_slack_message, dag=dag
)

[extract_total_sales_task, extract_brand_wise_sales_task] >> slack_task

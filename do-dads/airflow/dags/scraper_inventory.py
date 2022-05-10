import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

local_tz = pendulum.timezone("America/New_York")

with DAG(
    dag_id='scraper_inventory',
    schedule_interval='0 20 * * 3,6',
    start_date=pendulum.datetime(2021, 1, 1, tz=local_tz),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=5000),
    tags=['scraper'],
#    params={"example_key": "example_value"},
) as dag:
	t1 = BashOperator( \
	    task_id='inventory_switches', \
	    bash_command='python3 /opt/central_tools/scrapers/scraper_devices.py --dev_type switch --userID scraper', \
	    dag=dag)
	t2=  BashOperator( \
	    task_id='inventory_aps', \
	    bash_command='python3 /opt/central_tools/scrapers/scraper_devices.py --dev_type all_ap --userID scraper', \
	    dag=dag)

import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy import DummyOperator

local_tz = pendulum.timezone("America/New_York")

with DAG(dag_id='scraper', 
   schedule_interval='0 3 * * *', 
   start_date=pendulum.datetime(2021, 1, 1, tz=local_tz), 
   catchup=False, 
   dagrun_timeout=datetime.timedelta(minutes=5000), 
   tags=['scraper'],
) as dag:
    with TaskGroup(group_id='group1') as tg1:
          t1 = BashOperator( \
                 task_id='scraper_sites', \
                 bash_command='python3 /home/mgresham/central_tools/scrapers/scraper_sites.py', \
                 dag=dag)
          t2=  BashOperator( \
                 task_id='scraper_templates', \
                 bash_command='python3 /home/mgresham/central_tools/scrapers/scraper_templates.py', \
                 dag=dag)
          t3 = BashOperator( \
                 task_id='scraper_groups', \
                 bash_command='python3 /home/mgresham/central_tools/scrapers/scraper_groups.py', \
                 dag=dag)

    with TaskGroup(group_id='group2') as tg2:
          t5 = BashOperator( \
                task_id='scraper_switches', \
                bash_command='python3 /home/mgresham/central_tools/scrapers/scraper_switches.py', \
                dag=dag)
          t6 = BashOperator( \
                 task_id='scraper_aps', \
                 bash_command='python3 /home/mgresham/central_tools/scrapers/scraper_aps.py', \
                 dag=dag)
          t7 = BashOperator( \
                 task_id='scraper_ports', \
                 bash_command='python3 /home/mgresham/central_tools/scrapers/scraper_ports.py', \
                 dag=dag)
          t8 = BashOperator( \
                 task_id='scraper_variables', \
                 bash_command='python3 /home/mgresham/central_tools/scrapers/scraper_variables.py', \
                 dag=dag)
          t9 = BashOperator( \
                 task_id='scraper_get_commit', \
                 bash_command='python3 /home/mgresham/central_tools/scrapers/scraper_get_commit.py', \
                 dag=dag)

    with TaskGroup(group_id='group3') as tg3:
          t10 = BashOperator( \
                task_id='inventory_switches', \
                bash_command='python3 /home/mgresham/central_tools/scrapers/scraper_devices.py --dev_type switch --userID scraper', \
                dag=dag)
          t11 = BashOperator( \
                task_id='inventory_aps', \
                bash_command='python3 /home/mgresham/central_tools/scrapers/scraper_devices.py --dev_type all_ap --userID scraper', \
                dag=dag)

    tg1>>tg2>>tg3

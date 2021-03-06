/usr/bin/echo "============================================================"
/usr/bin/echo " Setting up airflow......"
/usr/bin/echo "============================================================"
sudo -u airflow -s
cd /opt/airflow
virtualenv airflow_virtualenv
cd /opt/airflow/airflow_virtualenv/bin
source activate
export AIRFLOW_HOME=/opt/airflow

# Install Airflow using the constraints file
pip install 'apache-airflow==2.3.0' \
	 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.3.0/constraints-3.7.txt"

# The Standalone command will initialise the database, make a user,
# and start all components for you.
airflow db init

/usr/bin/echo "Set a password for the airflow user account"
airflow users create \
	          --username admin \
		            --firstname FIRST_NAME \
			              --lastname LAST_NAME \
				                --role Admin \
						          --email admin@example.org

#exit the virtual environment
exit

/usr/bin/sudo /usr/bin/chown -R airflow:central_tools /opt/airflow

/usr/bin/sudo /usr/bin/cp /opt/central_tools/do-dads/airflow/airflow-webserver.service /etc/systemd/system/
/usr/bin/sudo /usr/bin/cp /opt/central_tools/do-dads/airflow/airflow-scheduler.service /etc/systemd/system/

/usr/bin/sudo /usr/bin/systemctl enable airflow-webserver.service
/usr/bin/sudo /usr/bin/systemctl enable airflow-scheduler.service

/usr/bin/sudo /usr/bin/systemctl start airflow-webserver.service
/usr/bin/sudo /usr/bin/systemctl start airflow-scheduler.service

#move the scraper DAGS
/usr/bin/sudo /usr/bin/cp -R /opt/central_tools/do-dads/airflow/dags /opt/airflow/dags
/usr/bin/sudo /usr/bin/chown -R airflow:central_tools /opt/airflow/dags/*.py


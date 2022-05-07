/usr/bin/echo "============================================================"
/usr/bin/echo " Installing directory structure and adding users......"
/usr/bin/echo "============================================================"

/usr/bin/sudo /usr/sbin/adduser --system --group --home /opt/central_tools central_tools
/usr/bin/sudo /usr/sbin/adduser --system --ingroup central_tools --home /opt/airflow airflow
/usr/bin/sudo mkdir /opt/central_tools
/usr/bin/sudo /usr/bin/chown central_tools:central_tools /opt/central_tools/


/usr/bin/sudo /usr/bin/systemctl stop apparmor
/usr/bin/sudo /usr/bin/systemctl disable apparmor
/usr/bin/sudo /usr/bin/apt remove --assume-yes --purge apparmor


/usr/bin/echo "============================================================"
/usr/bin/echo " Central Tools pre work......"
/usr/bin/echo "============================================================"
cd /opt/
/usr/bin/sudo /usr/bin/git clone https://github.com/micgresham/central_tools.git
/usr/bin/sudo /usr/bin/chown -R central_tools:central_tools /opt/central_tools/


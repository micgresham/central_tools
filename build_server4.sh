/usr/bin/echo "============================================================"
/usr/bin/echo " Setting up Central Tools......"
/usr/bin/echo "============================================================"
cd /opt/central_tools
/usr/bin/sudo /usr/bin/python3 -m venv env
 source env/bin/activate
 /usr/bin/pip3 install django==3.2.6
 /usr/bin/pip3 install -r requirements.txt
 /usr/bin/python3 manage.py makemigrations 
 /usr/bin/python3 manage.py migrate --database=auth_db
 /usr/bin/echo " "
 /usr/bin/echo "Create an account for the Central Tools administrator:"
 /usr/bin/python3 manage.py createsuperuser --database=auth_db

 #needed for gunicorn
 /usr/bin/sudo /usr/bin/pip install mysqlclient
 /usr/bin/sudo /usr/bin/pip install Pillow
 /usr/bin/sudo /usr/bin/pip install jsonfield
 /usr/bin/sudo /usr/bin/pip install whitenoise
 /usr/bin/sudo /usr/bin/pip3 install python-decouple
 /usr/bin/sudo /usr/bin/pip3 install unipath

export MY_IP=`/usr/bin/hostname -I | /usr/bin/sed -r 's/( )+//g'`

/usr/bin/sudo /usr/bin/cp -R /opt/central_tools/do-dads/nginx /etc
/usr/bin/sudo /usr/bin/sed -i 's/@@MY_IP@@/'"$MY_IP"'/' /etc/nginx/sites-available/central_tools.orig
/usr/bin/sudo /usr/bin/mv /etc/nginx/sites-available/central_tools.orig /etc/nginx/sites-available/central_tools

/usr/bin/sudo /usr/bin/rm -rf /etc/nginx/sites-enabled/central_tools
/usr/bin/sudo ln -s /etc/nginx/sites-available/central_tools /etc/nginx/sites-enabled

/usr/bin/sudo /usr/bin/cp /opt/central_tools/do-dads/gunicorn.service  /etc/systemd/system/gunicorn.service
/usr/bin/sudo /usr/bin/systemctl enable gunicorn.service
/usr/bin/sudo /usr/bin/systemctl start nginx
/usr/bin/sudo /usr/bin/systemctl start gunicorn.service
/usr/bin/sudo /usr/bin/systemctl status gunicorn.service
deactivate

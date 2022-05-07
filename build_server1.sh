/usr/bin/echo "============================================================"
/usr/bin/echo " Starting Central Tools install"
/usr/bin/echo " This install is currently based on: "
/usr/bin/echo "       ubuntu-22.04-live-server-amd64.iso"
/usr/bin/echo "============================================================"

/usr/bin/echo "============================================================"
/usr/bin/echo " Updating apt package manager......"
/usr/bin/echo "============================================================"

/usr/bin/sudo /usr/bin/apt -y update

/usr/bin/echo "============================================================"
/usr/bin/echo " Installing required packages......"
/usr/bin/echo "============================================================"

/usr/bin/sudo /usr/bin/apt -y install libmysqlclient-dev
/usr/bin/sudo /usr/bin/apt -y install libmysqlclient21:amd64
/usr/bin/sudo /usr/bin/apt -y install mysql-client
/usr/bin/sudo /usr/bin/apt -y install mysql-common
/usr/bin/sudo /usr/bin/apt -y install mysql-server


/usr/bin/sudo /usr/bin/apt -y install python3
/usr/bin/sudo /usr/bin/apt -y install python3-apt
/usr/bin/sudo /usr/bin/apt -y install python3-certifi
/usr/bin/sudo /usr/bin/apt -y install python3-cffi-backend
/usr/bin/sudo /usr/bin/apt -y install python3-chardet
/usr/bin/sudo /usr/bin/apt -y install python3-click
/usr/bin/sudo /usr/bin/apt -y install python3-colorama
/usr/bin/sudo /usr/bin/apt -y install python3-commandnotfound
/usr/bin/sudo /usr/bin/apt -y install python3-cryptography
/usr/bin/sudo /usr/bin/apt -y install python3-cupshelpers
/usr/bin/sudo /usr/bin/apt -y install python3-dbus
/usr/bin/sudo /usr/bin/apt -y install python3-dev
/usr/bin/sudo /usr/bin/apt -y install python3-dev default-libmysqlclient-dev build-essential
/usr/bin/sudo /usr/bin/apt -y install python3-distro
/usr/bin/sudo /usr/bin/apt -y install python3-distutils
/usr/bin/sudo /usr/bin/apt -y install python3-gdbm:amd64
/usr/bin/sudo /usr/bin/apt -y install python3-gi
/usr/bin/sudo /usr/bin/apt -y install python3-idna
/usr/bin/sudo /usr/bin/apt -y install python3-ldb
/usr/bin/sudo /usr/bin/apt -y install python3-lib2to3
/usr/bin/sudo /usr/bin/apt -y install python3-minimal
/usr/bin/sudo /usr/bin/apt -y install python3-netifaces
/usr/bin/sudo /usr/bin/apt -y install python3-pip
/usr/bin/sudo /usr/bin/apt -y install python3-pkg-resources
/usr/bin/sudo /usr/bin/apt -y install python3-requests
/usr/bin/sudo /usr/bin/apt -y install python3-setuptools
/usr/bin/sudo /usr/bin/apt -y install python3-six
/usr/bin/sudo /usr/bin/apt -y install python3-talloc:amd64
/usr/bin/sudo /usr/bin/apt -y install python3-urllib3
/usr/bin/sudo /usr/bin/apt -y install python3-wheel
/usr/bin/sudo /usr/bin/apt -y install python3-xkit
/usr/bin/sudo /usr/bin/apt -y install python3-yaml
/usr/bin/sudo /usr/bin/apt -y install python3.8
/usr/bin/sudo /usr/bin/apt -y install python3.8-dev
/usr/bin/sudo /usr/bin/apt -y install python3.8-minimal
/usr/bin/sudo /usr/bin/apt -y install python3-virtualenv
/usr/bin/sudo /usr/bin/apt -y install python3.10-venv
/usr/bin/sudo /usr/bin/apt -y install nginx
/usr/bin/sudo /usr/bin/apt -y install gunicorn


/usr/bin/echo "============================================================"
/usr/bin/echo " Setting up mysql......"
/usr/bin/echo "============================================================"
/usr/bin/sudo systemctl stop mysql
/usr/bin/sudo mkdir /opt/mysql
#/usr/bin/sudo mkdir /opt/mysql/mysql
#/usr/bin/sudo mkdir /opt/mysql/mysql/data
/usr/bin/sudo /usr/bin/chown -R mysql:mysql /opt/mysql/
/usr/bin/sudo /usr/bin/chmod -R 755 /opt/mysql/
/usr/bin/sudo /usr/bin/cp /opt/central_tools/do-dads/mysql/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
/usr/bin/sudo /usr/bin/cp /opt/central_tools/do-dads/mysql/reader.cnf /etc/mysql/reader.cnf
/usr/bin/sudo /usr/bin/cp /opt/central_tools/do-dads/mysql/scraper.cnf /etc/mysql/scraper.cnf
/usr/bin/sudo /usr/bin/cp /opt/central_tools/do-dads/mysql/ct_gui_admin.cnf /etc/mysql/ct_gui_admin.cnf
/usr/bin/sudo /usr/bin/cp /opt/central_tools/do-dads/mysql/ct_gui.cnf /etc/mysql/ct_gui.cnf

/usr/bin/echo "Initializing the mySQL system...."
/usr/bin/sudo -u mysql /usr/sbin/mysqld --initialize --user=mysql --basedir=/opt/mysql --datadir=/opt/mysql/data

export myPasswd="`/usr/bin/sudo /usr/bin/grep root@localhost: /var/log/mysql/error.log | /usr/bin/tail -1 | cut -d : -f 4-`"
export myPasswd=`echo $myPasswd | sed 's/ *$//g'`
sleep 5
/usr/bin/echo " "
/usr/bin/echo " "
/usr/bin/sudo systemctl start mysql
sleep 5
/usr/bin/echo "Random temporary password is: $myPasswd"
/usr/bin/echo "Your mysql root password has been changed to .Buttercup!"
/usr/bin/mysql -u root -p$myPasswd --connect-expired-password --execute="ALTER USER 'root'@'localhost' IDENTIFIED BY '.Butt3rcup!';"
/usr/bin/echo "****** Your should change this to something more secure!! ******"
/usr/bin/echo " "
/usr/bin/echo "To change you root password:"
/usr/bin/echo "   mysql -u root -p"
/usr/bin/echo "      ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewPassword'"
/usr/bin/echo ""
/usr/bin/echo "Importing Central Tools schema...."
/usr/bin/mysql -u root -p.Butt3rcup! < /opt/central_tools/central_tools.sql
/usr/bin/mysql -u root -p.Butt3rcup! < /opt/central_tools/users.sql
/usr/bin/echo " "
/usr/bin/echo " "


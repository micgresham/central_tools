# Initial setup

## Get the code
<br>
git clone https://github.com/micgresham/central_tools.git<br>
cd central-tools<br>

## Virtualenv modules installation (Unix based systems)
<br>
python3 -m venv env<br>
source env/bin/activate<br>
pip3 install django==3.2.6<br>
pip3 install -r requirements.txt<br>

## Build the default database with the built-in admin superuser
<br>
Username: admin<br>
Password: aruba123<br>
<br>
This user will have access to the /admin/ user and group functions

## purge the database (if it exists)
<br>
rm -rf db.sqlite3<br>

## create the superuser
<br>
python manage.py createsuperuser

## Start the application (development mode)
<br>
python manage.py runserver # default port 8000<br>

## Start the app - custom port
<br>
python manage.py runserver 0.0.0.0:your_port <br>
<br>
Access the web app in browser: http://127.0.0.1:8000/<br>


## Howto add tasks
<pre>
Adding a task:
	1) Create a workflow file in apps/home/
	2) Create the workflow pathin apps/home/urls.py
	4) Create one or more templates for the workflow in apps/templates/home
	5) Edit the sidebar.html file in apps/templates/includes to place links for the workflow on the side menu
</pre>

## Credits & Links

<br />

### Datta Able Free Dashboard
### [Django Admin Dashboards](https://appseed.us/admin-dashboards/django)

Datta Able Bootstrap Lite is the most styled Bootstrap 4 Lite Admin Template, around all other Lite/Free admin templates in the market. It comes with high feature-rich pages and components with fully developer-centric code. Comes with error/bug-free, well structured, well-commented code and regularly with all latest updated code, which saves your large amount of developing backend application time and it is fully customizable. - provided by **CodedThemes**.

<br />

---



# Central Tools

Central Tools is a tool framework designed to work with Aruba's Central management platform.<br>  
Central Tools performs two (2) primary functions:<br>

<li>Collection of data using "scrapers" and stores it to an interchange database.  This allows for rapid queries of without the penalty of API calls and the use of complex SQL statements</li>
<li>A framework for "workflow" tasks to speed certain activities normally done via the Central gui."

<p>Aruba Central is a product of HPE/Aruba and is copyright/trademark HPE/Aruba.  Central Tools interacts with Aruba Central as an end user in accordance with the Central EULA.</p>

# Initial setup

Please review the build_server scripts 1-5.  These will install and configure Central Tools along with mySQL and Apache Airflow.


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


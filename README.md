# Initial setup

## Get the code
<br>
git clone https://github.com/micgesham/central_tools.git<br>
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

## create the db and load the default build
<br>
sqlite3 db.sqlite3 < central-tools_default.sql<br>

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
	1) Create entry in apps/home/forms.py
	2) Create entry in apps/home/views.py
	3) Create entry in apps/home/urls.py
	4) Create a template in  apps/templates/home
	5) Edit the sidebar.html file in apps/templates/includes
</pre>

## Example: Creating a task to create a template group and adding a template file in one action

<h2>apps/home/forms.py</h2>

<pre><code>
class CreateTgroupForm(forms.Form):
    ARCH_CHOICE =(
       ("Instant", "Instant"),
       ("AOS10", "AOS10"),
    )
    AP_ROLE_CHOICE =(
       ("Standard", "Standard"),
       ("Microbranch", "Microbranch"),
    )
    GW_ROLE_CHOICE =(
       ("BranchGateway", "Branch Gateway"),
       ("VPNConcentrator", "VPN Concentrator"),
       ("WLANGateway", "WLAN Gateway"),
    )
    DEV_TYPE_CHOICE =(
       ("AccessPoints", "Access Points"),
       ("Gateways", "Gateways"),
       ("Switches", "Switches"),
    )
    SW_TYPE_CHOICE =[
       ("AOS_S", "AOS-S"),
       ("AOS_CX", "CX"),
    ]
    TGROUP_CHOICE =(
       ("Wired", "Wired"),
       ("Wireless", "IAP and Gateway"),
    )
    TDEV_TYPE_CHOICE =(
       ("CX", "CX"),
       ("ArubaSwitch", "Aruba Switch"),
       ("IAP", "IAP"),
       ("MobilityController", "Mobility Controller"),
    )


    Tgroup_name = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Template Group Name', 'class': 'form-control',
       }))

    template = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    Tmodel = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': '6300', 'class': 'form-control',
       }))

    Tversion = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ALL', 'class': 'form-control',
       }))

    TDevType = forms.ChoiceField(
         required=True,
         choices = TDEV_TYPE_CHOICE,
         )

    TgroupTypes = forms.MultipleChoiceField(
         required=True,
         choices = TGROUP_CHOICE,
         widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
         )
    
    AllowedDeviceTypes = forms.MultipleChoiceField(
         choices = DEV_TYPE_CHOICE,
         widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
         )
    Architecture = forms.ChoiceField(choices = ARCH_CHOICE)
    ApNetworkRole = forms.ChoiceField(choices = AP_ROLE_CHOICE,
         widget=forms.Select(),
         )
    GwNetworkRole = forms.ChoiceField(choices = GW_ROLE_CHOICE,
         widget=forms.Select(),
         )
    AllowedSwitchTypes = forms.MultipleChoiceField(
         required='required',
         choices = SW_TYPE_CHOICE,
         widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
         )

</code></pre>


<h2>apps/templates/includes/sidebar.html</h2>

<pre>
  &lt;li class="nav-item pcoded-menu-caption"&gt;
      &lt;label&gt;Tasks&lt;/label&gt;
  &lt;/li&gt;
  &lt;li data-username="Create template group and upload a template"
      class="nav-item {% if 'ui-forms' in segment %} active {% endif %}"&gt;
      &lt;a href="/create_tgroup/" class="nav-link "&gt;&lt;span class="pcoded-micon"&gt;&lt;i class="feather icon-file-text"&gt;&lt;/i&gt;&lt;/span&gt;&lt;span class="pcoded-mtext"&gt;Create TG and Upload Template&lt;/span&gt;&lt;/a&gt;
 &lt;/li&gt;
</pre>

<h2>apps/home/urls.py</h2>

<pre><code>
urlpatterns = [

    # The home page
    path('', views.home, name='home'),

    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('test_central/', test_central, name='test_central'),

# Put your tasks here
    path('create_tgroup/', create_tgroup, name='create_tgroup'),

    # Matches any html file
    re_path(r'^.*\.htm', views.pages, name='pages'),
    re_path(r'^.*\.html', views.pages, name='pages')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

</code></pre>

<h2>apps/home/views.py</h2>

<pre><code>
@login_required
def create_tgroup(request):

    if request.method == 'POST':
      if __debug__:
        print("create_tgroup POST")

      form = CreateTgroupForm(request.POST, request.FILES)

      if form.is_valid():

         myfile = request.FILES['template']
         fs = FileSystemStorage()
         filename = fs.save('templates/' + myfile.name, myfile)

         TgroupName = request.POST.get('Tgroup_name')
         TgroupTypes = request.POST.getlist('TgroupTypes')
         TDevType = request.POST.get('TDevType')
         Tmodel = request.POST.get('Tmodel')
         Tversion = request.POST.get('Tversion')
         Architecture = request.POST.get('Architecture')
         AllowedDeviceTypes = request.POST.getlist('AllowedDeviceTypes')
         AllowedSwitchTypes = request.POST.getlist('AllowedSwitchTypes')
         GwNetworkRole = request.POST.get('GwNetworkRole')
         ApNetworkRole = request.POST.get('ApNetworkRole')

         if __debug__:
           print(myfile.name)

         #Create the initial JSON structure

         data_set = { "group": TgroupName, "group_attributes": { "template_info": { "Wired": True, "Wireless": True }, "group_properties": { "AllowedDevTypes": AllowedDeviceTypes, "Architecture": Architecture, "ApNetworkRole": ApNetworkRole, "GwNetworkRole": GwNetworkRole, "AllowedSwitchTypes": AllowedSwitchTypes } } }
         data_dump  = json.dumps(data_set)
         data = json.loads(data_dump)

         if __debug__:
           print(data)

         #call test_central to verify our connection and refresh the tokens if needed
         test_central(request)

         #get the access token from the user profile
         current_user = request.user.profile
         access_token = current_user.central_token
         central_url = current_user.central_url

         #**********************************
         #make API call to create the group         
         #**********************************
         api_url = central_url + "/configuration/v3/groups"

         #is out token valid?
         qheaders = {
           "Content-Type":"application/json",
           "Authorization": "Bearer " + access_token,
         }

         qparams = {
           "limit": 1,
           "offset": 0
         }

         response = requests.request("POST", api_url, headers=qheaders, json=data)
         
         if __debug__:
           print(response)
           print(response.text.encode('utf8'))
 
         if "Created" in response.json():
            messages.success(request, 'Group ' + TgroupName + ' created ')

            #**********************************
            #make API call to add the template to the group         
            #**********************************
            api_url = central_url + "/configuration/v1/groups/" + TgroupName + "/templates"

            # do not put 'Content-Type': 'application/json' in the headers.  It will cause fordata errors
            qheaders={
               "Authorization": "Bearer " + access_token,
            }
            qparams={
                "name": urllib.parse.quote_plus(myfile.name),
                "device_type": TDevType,
                "version": Tversion,
                "model": Tmodel,
            }
            qpayload={}
            qfiles=[
               ('template',(myfile.name,open(settings.MEDIA_ROOT + '/' + filename,'rb'),'text/plain'))
            ]

            # call the API and send the template file to the group
            response = requests.request("POST", api_url, params=qparams, headers=qheaders, data=qpayload, files=qfiles)
            if "Created" in response.json():
               messages.success(request, 'Template ' + myfile.name + ' uploaded. ')
            else:
               messages.warning(request, 'Template ' + myfile.name + " not uploaded to group " + TgroupName)
                
            if __debug__:
              print(response.text.encode('utf8'))

            # return from whence thy came
            context = {}
            context['form'] = CreateTgroupForm()
            return render( request, "home/create_tgroup.html", context)

         else:
            messages.warning(request, 'Group ' + TgroupName + ' creation failed. ' + response.text)
 
            context = {}
            context['form'] = CreateTgroupForm()
            return render( request, "home/create_tgroup.html", context)
      else:
         context = {}
         context['form'] = CreateTgroupForm()
         return render( request, "home/create_tgroup.html", context)

    else:
      context = {}
      context['form'] = CreateTgroupForm()
      return render( request, "home/create_tgroup.html", context)
</code></pre>

## Credits & Links

<br />

### Datta Able Free Dashboard
### [Django Admin Dashboards](https://appseed.us/admin-dashboards/django)

Datta Able Bootstrap Lite is the most styled Bootstrap 4 Lite Admin Template, around all other Lite/Free admin templates in the market. It comes with high feature-rich pages and components with fully developer-centric code. Comes with error/bug-free, well structured, well-commented code and regularly with all latest updated code, which saves your large amount of developing backend application time and it is fully customizable. - provided by **CodedThemes**.

<br />

---


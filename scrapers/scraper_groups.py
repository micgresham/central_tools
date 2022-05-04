#!/usr/bin/env python3

import datetime
import mysql.connector
import json
import requests
from pycentral.base import ArubaCentralBase
from pycentral.configuration import Groups
from central_test_mysql import test_central

def sqlescape(string):
   if (string == None):
     return ""
   else:
     clean_str = string.translate(string.maketrans({
            "\0": "\\0",
            "\r": "\\r",
            "\x08": "\\b",
            "\x09": "\\t",
            "\x1a": "\\z",
            "\n": "\\n",
            "\r": "\\r",
            "\"": "",
            "'": "''",
            "\\": "\\\\",
            "%": "\\%"
        }))
     return clean_str

def sqlboolean(bool_val):
   return(int(bool_val == True))


def get_all_groups (central,loop_limit=0):
    """ Get all groups and return a flattened group list """
    # set initial vars
    print ("Getting groups")
    limit = 20
    g = Groups()
    full_group_list = []

    # loop through call to get groups appending groups to full group list
    # stop when response is empty
    counter = 0
    need_more = True

    while need_more:
        response = g.get_groups(central,offset=counter,limit=limit)
        if response['msg']['data'] != []:
            full_group_list = full_group_list + response['msg']['data']
        elif response['msg']['data'] == []:
            need_more = False
            break
        else:
            print("ERROR")
            need_more = False
            print(response)
            break
        counter = counter + limit
        print(counter)

#exit the function after loop_limit runs...for testing 
        if (loop_limit != 0):
          if (loop_limit <= counter):
            need_more = False    

    full_group_list_flat = [item for sublist in full_group_list for item in sublist]
    return full_group_list_flat


def get_group_properties (central_info,group):
    # set initial vars
    print ("Getting group info for " + group)
    limit = 20
    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "/configuration/v1/groups/properties"
    qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
      "limit": "1"
    }

    group_config = []
    group_list = []
    group_list += [group]

    qparams = {
      "groups": group_list,
    }

    response = requests.request("GET", api_function_url, headers=qheaders, params=qparams)
    if "error" in response.json():
      return "{'ERROR'}"
    else:
#      print(response.json())
      return response.json()



central_info = test_central()
#print("--------------")
#print(central_info)
#print("--------------")

ssl_verify=True
# set Central data
central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
    
# get all device variables - this call takes some time
data_dict = get_all_groups(central)
#print(data_dict)

cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
cursor = cnx.cursor()

# iterate all the nested dictionaries with keys
for i in data_dict:
  # display
    group_name = sqlescape(i)
    group_properties = get_group_properties(central_info,group_name)
#    print(group_properties['data'][0]['properties'])
    AOSVersion = group_properties['data'][0]['properties']['AOSVersion']
    AllowedDevTypes = json.dumps(group_properties['data'][0]['properties']['AllowedDevTypes'])
    AllowedSwitchTypes = json.dumps(group_properties['data'][0]['properties']['AllowedSwitchTypes'])
    if "ApNetworkRole" in group_properties['data'][0]['properties']:
       ApNetworkRole = group_properties['data'][0]['properties']['ApNetworkRole']
    else:
       ApNetworkRole = ""

    if "Architecture" in group_properties['data'][0]['properties']:
       Architecture = group_properties['data'][0]['properties']['Architecture']
    else:
       Architecture = "" 

    if "GwNetworkRole" in group_properties['data'][0]['properties']:
      GwNetworkRole = group_properties['data'][0]['properties']['GwNetworkRole']
    else: 
      GwNetworkRole = ""

    MonitorOnly = json.dumps(group_properties['data'][0]['properties']['MonitorOnly'])
    MonitorOnlySwitch = sqlboolean(group_properties['data'][0]['properties']['MonitorOnlySwitch'])
#    print(AOSVersion)
#    print(AllowedDevTypes)
#    print(AllowedSwitchTypes)
#    print(ApNetworkRole)
#    print(Architecture)
#    print(GwNetworkRole)
#    print(MonitorOnly)
#    print(MonitorOnlySwitch)
    queryU1 = "INSERT INTO central_tools.groups (customer_id,group_name,last_refreshed, \
		AOSVersion, \
		AllowedDevTypes, \
		AllowedSwitchTypes, \
		ApNetworkRole, \
		Architecture, \
		GwNetworkRole, \
		MonitorOnly, \
		MonitorOnlySwitch) \
               VALUES ('{0}','{1}',now(),'{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')".format( \
                central_info['customer_id'],group_name, \
		AOSVersion, \
		AllowedDevTypes, \
		AllowedSwitchTypes, \
		ApNetworkRole, \
		Architecture, \
		GwNetworkRole, \
		MonitorOnly, \
		MonitorOnlySwitch)

    query = queryU1 + " ON DUPLICATE KEY UPDATE  \
		group_name = '{0}', \
		AOSVersion = '{1}', \
		AllowedDevTypes = '{2}', \
		AllowedSwitchTypes = '{3}', \
		ApNetworkRole = '{4}', \
		Architecture = '{5}', \
		GwNetworkRole = '{6}', \
		MonitorOnly = '{7}', \
		MonitorOnlySwitch = '{8}', \
		last_refreshed = now()".format( \
                group_name, \
		AOSVersion, \
		AllowedDevTypes, \
		AllowedSwitchTypes, \
		ApNetworkRole, \
		Architecture, \
		GwNetworkRole, \
		MonitorOnly, \
		MonitorOnlySwitch)

#    print("------------------------")
#    print(query)

    cursor.execute(query)
    cnx.commit()
     
cursor.close()
cnx.close()

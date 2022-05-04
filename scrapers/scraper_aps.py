#!/usr/bin/env python3

import argparse
import datetime
import mysql.connector
import json
import requests
import re
import time 

from pycentral.base import ArubaCentralBase
#from pycentral.configuration import Groups
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


def get_aps (central, loop_limit=0):
    # set initial vars
    print ("Getting APs")

    # loop through call to get devices
    # stop when response is empty
    counter = 0
    need_more = True

    limit = 1000
    offset = 0
    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "monitoring/v2/aps"
    qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
    }

    device_list = []

    while need_more:
        qparams = {
          "limit": limit,
          "offset": offset,
          "show_resources": "True",
          "calculate_client": "True"
        }

        response = requests.request("GET", api_function_url, headers=qheaders, params=qparams)
        if response.json()['aps'] != []:
            device_list = device_list + response.json()['aps']
            offset += limit
        elif response.json()['aps'] == []:
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

    return device_list

def get_ap_details (central, serial, loop_limit=0):
    # set initial vars
    print ("Getting config details for " + serial)

    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "monitoring/v1/aps/{0}".format(serial)
    qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
    }

    qparams = {
      "details": 'false',
    }

#    print(api_function_url)
    response = requests.request("GET", api_function_url, headers=qheaders, params=qparams)
#    if "error" in response.json():
#      return "{'ERROR'}"
#    else:


    if (response.status_code == 200):
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_response_status = json.loads(response_status) 
      j_result = response.json()
      j_result.update(j_response_status)



    elif (response.status_code == 401): # authentication timed out
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_result = json.loads(response_status) 
   
    elif (response.status_code == 500):
       print(response.text)
       error_str = '{ "Error": 1, "Error_text": "' + response.json()['description'] + '" }'
       result_str = '{"chassis_type": "False", "cpu_utilization": 0, "default_gateway": "na", "device_mode": 0, "fan_speed": "Ok", "firmware_version": "na", "group_name": "na", "ip_address": "na", "labels": [], "macaddr": "na", "max_power": 0, "mem_free": 0, "mem_total": 0, "model": "na", "name": "na", "poe_consumption": "0", "power_consumption": 0, "na": "na", "serial": "na", "site": "na", "stack_id": "na", "status": "na", "switch_type": "na", "temperature": "0", "total_clients": 0, "updated_at": 0, "uplink_ports": [], "uptime": 0, "usage": 0}'
       j_result = json.loads(result_str)
       error_str = '{ "Error": 1, "Error_text": "Internal server error"}'
       response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
       j_response_status = json.loads(response_status) 
       j_error = json.loads(error_str)
       j_result.update(j_error)
       j_result.update(j_response_status)
       print(response.headers)
    return j_result 


#    print(api_function_url)
    response = requests.request("GET", api_function_url, headers=qheaders, params=qparams)
#    if "error" in response.json():
#      return "{'ERROR'}"
#    else:


    if (response.status_code == 200):
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_response_status = json.loads(response_status) 
      j_result = response.json()
      j_result.update(j_response_status)



    elif (response.status_code == 401): # authentication timed out
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_result = json.loads(response_status) 


    return j_result 



parser = argparse.ArgumentParser()
parser.add_argument('--userID', \
                     default = 'scraper', \
                     help='Central Tools user ID to use for API access')
args = parser.parse_args()
userID = args.userID

print("Accessing API as " + userID)
central_info = test_central(userID)
#print("--------------")
#print(central_info)
#print("--------------")

ssl_verify=True
# set Central data
central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
    
# get all device variables - this call takes some time
data_dict =[] 
data_dict = get_aps(central)
print("Sleeping 10 seconds to keep the API happy....")
#time.sleep(10)

customer_id = central_info['customer_id']

cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
cursor = cnx.cursor()
if (len(data_dict) > 0):
  # iterate all the nested dictionaries with keys
  for i in data_dict:
     ap_deployment_mode = i['ap_deployment_mode']
     ap_group = i['ap_group']
     cluster_id = i['cluster_id']
     firmware_version = i['firmware_version']
     gateway_cluster_id = i['gateway_cluster_id']
     gateway_cluster_name = i['gateway_cluster_name']
     group_name = i['group_name']
     ip_address = i['ip_address']
     labels = i['labels']
     macaddr = i['macaddr']
     mesh_role =  i['mesh_role']
     model = i['model']
     name = i['name']
     notes = i['notes']
     public_ip_address = i['public_ip_address']
     radios = json.dumps(i['radios'])
     serial = i['serial']
     site_name = i['site']
     status = i['status']
     subnet_mask = i['subnet_mask']
     swarm_id = i['swarm_id']
     swarm_master = sqlboolean(i['swarm_master'])
     swarm_name = i['swarm_name']
     
     print(site_name)

     queryU1 = "INSERT INTO central_tools.aps ( \
        ap_deployment_mode, \
        ap_group, \
        cluster_id, \
        firmware_version, \
        gateway_cluster_id, \
        gateway_cluster_name, \
        group_name, \
        ip_address, \
        labels, \
        macaddr, \
        mesh_role, \
        model, \
        name, \
        notes, \
        public_ip_address, \
        radios, \
        serial, \
        site_name, \
        status, \
        subnet_mask, \
        swarm_id, \
        swarm_master, \
        swarm_name, \
        customer_id, \
	last_refreshed) \
       VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',\
       '{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}',\
       {21},'{22}','{23}',\
       now())".format( \
        ap_deployment_mode, \
        ap_group, \
        cluster_id, \
        firmware_version, \
        gateway_cluster_id, \
        gateway_cluster_name, \
        group_name, \
        ip_address, \
        labels, \
        macaddr, \
        mesh_role, \
        model, \
        name, \
        notes, \
        public_ip_address, \
        radios, \
        serial, \
        site_name, \
        status, \
        subnet_mask, \
        swarm_id, \
        swarm_master, \
        swarm_name, \
        customer_id)

     query = queryU1 + " ON DUPLICATE KEY UPDATE  \
        ap_deployment_mode = '{0}', \
        ap_group = '{1}', \
        cluster_id = '{2}', \
        firmware_version = '{3}', \
        gateway_cluster_id = '{4}', \
        gateway_cluster_name = '{5}', \
        group_name = '{6}', \
        ip_address = '{7}', \
        labels = '{8}', \
        macaddr = '{9}', \
        mesh_role = '{10}', \
        model = '{11}', \
        name = '{12}', \
        notes = '{13}', \
        public_ip_address = '{14}', \
        radios = '{15}', \
        serial = '{16}', \
        site_name = '{17}', \
        status = '{18}', \
        subnet_mask = '{19}', \
        swarm_id = '{20}', \
        swarm_master = {21}, \
        swarm_name = '{22}', \
        customer_id = '{23}', \
	last_refreshed = now()".format( \
        ap_deployment_mode, \
        ap_group, \
        cluster_id, \
        firmware_version, \
        gateway_cluster_id, \
        gateway_cluster_name, \
        group_name, \
        ip_address, \
        labels, \
        macaddr, \
        mesh_role, \
        model, \
        name, \
        notes, \
        public_ip_address, \
        radios, \
        serial, \
        site_name, \
        status, \
        subnet_mask, \
        swarm_id, \
        swarm_master, \
        swarm_name, \
        customer_id)
        
#     print("------------------------")
#     print(query)


     cursor.execute(query)
     cnx.commit()

     # Update the device table with the site name
     query = "UPDATE central_tools.devices SET site_name = '{0}' WHERE serial = '{1}'".format(site_name,serial) 
     cursor.execute(query)
     cnx.commit()

     

cursor.close()
cnx.close()

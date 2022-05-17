#!/usr/bin/env python3

import argparse
import datetime
import mysql.connector
import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
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


def get_switches (central, loop_limit=0):
    # set initial vars
    print ("Getting switches")

    # loop through call to get devices
    # stop when response is empty
    counter = 0
    need_more = True

    limit = 1000
    offset = 0
    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "monitoring/v1/switches"
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
        if response.json()['switches'] != []:
            device_list = device_list + response.json()['switches']
            offset += limit
        elif response.json()['switches'] == []:
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

def get_switch_details (central, serial, loop_limit=0):
    # set initial vars
    print ("Getting config details for " + serial)

    s = requests.Session()

    retries = Retry(total=5,
                backoff_factor=1,
                status_forcelist=[ 502, 503, 504 ])

    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.mount('http://', HTTPAdapter(max_retries=retries))

    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "/monitoring/v1/switches/{0}".format(serial)
    qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
    }

    qparams = {
      "details": 'false',
    }

#    print(api_function_url)
    response = s.request("GET", api_function_url, headers=qheaders, params=qparams)
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
   
    elif (response.status_code == 404):
       print(response.text)
       result_str = '{"chassis_type": "False", "cpu_utilization": 0, "default_gateway": "na", "device_mode": 0, "fan_speed": "Ok", "firmware_version": "na", "group_name": "na", "ip_address": "na", "labels": [], "macaddr": "na", "max_power": 0, "mem_free": 0, "mem_total": 0, "model": "na", "name": "na", "poe_consumption": "0", "power_consumption": 0, "na": "na", "serial": "na", "site": "na", "stack_id": "na", "status": "na", "switch_type": "na", "temperature": "0", "total_clients": 0, "updated_at": 0, "uplink_ports": [], "uptime": 0, "usage": 0}'
       j_result = json.loads(result_str)
       error_str = '{ "Error": 404, "Error_text": Page not found"}'
       response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
       j_response_status = json.loads(response_status) 
       j_error = json.loads(error_str)
       j_result.update(j_error)
       j_result.update(j_response_status)
       print(response.headers)
    elif (response.status_code == 500):
       print(response.text)
       result_str = '{"chassis_type": "False", "cpu_utilization": 0, "default_gateway": "na", "device_mode": 0, "fan_speed": "Ok", "firmware_version": "na", "group_name": "na", "ip_address": "na", "labels": [], "macaddr": "na", "max_power": 0, "mem_free": 0, "mem_total": 0, "model": "na", "name": "na", "poe_consumption": "0", "power_consumption": 0, "na": "na", "serial": "na", "site": "na", "stack_id": "na", "status": "na", "switch_type": "na", "temperature": "0", "total_clients": 0, "updated_at": 0, "uplink_ports": [], "uptime": 0, "usage": 0}'
       j_result = json.loads(result_str)
       error_str = '{ "Error": 1, "Error_text": "Internal server error"}'
       response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
       j_response_status = json.loads(response_status) 
       j_error = json.loads(error_str)
       j_result.update(j_error)
       j_result.update(j_response_status)
       print(response.headers)
    else:
       print(response.status_code)
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

def get_stack_details (central,stack_id):
    # set initial vars
    print ("Getting stack details for " + stack_id)
    s = requests.Session()

    retries = Retry(total=5,
                backoff_factor=1,
                status_forcelist=[ 502, 503, 504 ])

    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.mount('http://', HTTPAdapter(max_retries=retries))

    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "/monitoring/v1/switch_stacks/" + stack_id
    qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
    }

    qparams = {
    }

    response = s.request("GET", api_function_url, headers=qheaders, params=qparams)

    if (response.status_code == 200):
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_response_status = json.loads(response_status) 
      j_result = response.json()
      j_result.update(j_response_status)



    elif (response.status_code == 401): # authentication timed out
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_result = json.loads(response_status) 

    else: #something else went wrong 
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
data_dict = get_switches(central)
print("Sleeping 10 seconds to keep the API happy....")
time.sleep(10)

customer_id = central_info['customer_id']

cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
cursor = cnx.cursor()
if (len(data_dict) > 0):
  # iterate all the nested dictionaries with keys
  for i in data_dict:
    # display
    firmware_version = i['firmware_version']
    group_id = i['group_id']
    group_name = i['group_name']
    ip_address = i['ip_address']
    label_ids = i['labels']
    macaddr = i['macaddr']
    model = i['model']
    name = i['name']
    public_ip_address = i['public_ip_address']
    serial = i['serial']
    site_name = i['site']
    stack_id = i['stack_id']
    status = i['status']
    switch_type = i['switch_type']
    if i['uplink_ports'] == None:
      uplink_ports = json.dumps("[]")
    else:
     uplink_ports = i['uplink_ports']
   
    print(i)
    if "usage" in i:
      usage_int = i['usage']
    else:
      usage_int = 0
  
    data2 = get_switch_details(central,serial)

    if data2['status_code'] == 401:
      print("=============================")
      print(" Reauthenticating to Central")
      print("=============================")
      central_info = test_central(userID)
      central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
      data2 = get_switch_details(central,serial)

    chassis_type = sqlboolean(data2['chassis_type'])
    cpu_utilization = data2['cpu_utilization']
    default_gateway = data2['default_gateway']
    device_mode = data2['device_mode']

    if (data2['fan_speed'] == '-'):
      fan_speed = 0
    else: 
      fan_speed = data2['fan_speed']

    ip_address = data2['ip_address']
    mac_address = data2['macaddr']
    max_power = data2['max_power']
    mem_free = data2['mem_free']
    mem_total = data2['mem_total']
    
    if (data2['poe_consumption'] == '-'):
       poe_consumption = 0
    else:  
      poe_consumption = data2['poe_consumption']
    if (data2['power_consumption'] == None):
      power_consumption = 0
    else:
      power_consumption = data2['power_consumption']

    if (data2['temperature'] == 'None'):
      temperature = 0
    elif (data2['temperature'] == '-'):
      temperature = 0
    else:
      temperature = data2['temperature']

    total_clients = data2['total_clients']
    updated_at = "FROM_UNIXTIME(" + str(data2['updated_at']) + ")"

    if (data2['uptime'] == 'None'):
      uptime = 0
    if data2['uptime'] is None:
      uptime = 0
    else: 
      uptime = data2['uptime']
 
    if (stack_id != None): 
      data2 = get_stack_details(central,stack_id)

      if data2['status_code'] == 401:
        print("=============================")
        print(" Reauthenticating to Central")
        print("=============================")
        central_info = test_central(userID)
        central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
        data2 = get_stack_details(central,stack_id)
  
      if 'mac' in data2:
        commander_mac = data2['mac']
      else:
        commander_mac = ""
    else:
      commander_mac = ""


    queryU1 = "INSERT INTO central_tools.switches ( \
		firmware_version, \
		group_id, \
		group_name, \
		ip_address, \
		label_ids, \
		macaddr, \
		model, \
		name, \
		public_ip_address, \
		serial, \
		site_name, \
		stack_id, \
		status, \
		switch_type, \
		uplink_ports, \
		usage_int, \
		chassis_type, \
		commander_mac, \
		cpu_utilization, \
		default_gateway, \
		device_mode, \
		fan_speed, \
		max_power, \
		mem_free, \
		mem_total, \
		poe_consumption, \
		power_consumption, \
		temperature, \
		total_clients, \
		updated_at, \
		uptime, \
                customer_id, \
		last_refreshed) \
             VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',\
		'{10}','{11}','{12}','{13}','{14}',{15},{16},'{17}',{18},'{19}','{20}',\
		'{21}',{22},{23},{24},{25},{26},{27},{28},{29},{30},'{31}',\
                now())".format( \
		firmware_version, \
		group_id, \
		group_name, \
		ip_address, \
		label_ids, \
		macaddr, \
		model, \
		name, \
		public_ip_address, \
		serial, \
		site_name, \
		stack_id, \
		status, \
		switch_type, \
		uplink_ports, \
		usage_int, \
		chassis_type, \
		commander_mac, \
		cpu_utilization, \
		default_gateway, \
		device_mode, \
		fan_speed, \
		max_power, \
		mem_free, \
		mem_total, \
		poe_consumption, \
		power_consumption, \
		temperature, \
		total_clients, \
		updated_at, \
		uptime, \
                customer_id)

    query = queryU1 + " ON DUPLICATE KEY UPDATE  \
		firmware_version = '{0}', \
		group_id = '{1}', \
		group_name = '{2}', \
		ip_address = '{3}', \
		label_ids = '{4}', \
		macaddr = '{5}', \
		model = '{6}', \
		name = '{7}', \
		public_ip_address = '{8}', \
		serial = '{9}', \
		site_name = '{10}', \
		stack_id = '{11}', \
		status = '{12}', \
		switch_type = '{13}', \
		uplink_ports = '{14}', \
		usage_int = {15}, \
		chassis_type = {16}, \
		commander_mac = '{17}', \
		cpu_utilization = {18}, \
		default_gateway = '{19}', \
		device_mode = {20}, \
		fan_speed = '{21}', \
		max_power = {22}, \
		mem_free = {23}, \
		mem_total = {24}, \
		poe_consumption = {25}, \
		power_consumption = {26}, \
		temperature = {27}, \
		total_clients = {28}, \
		updated_at = {29}, \
		uptime = {30}, \
                customer_id = '{31}', \
		last_refreshed = now()".format( \
		firmware_version, \
		group_id, \
		group_name, \
		ip_address, \
		label_ids, \
		macaddr, \
		model, \
		name, \
		public_ip_address, \
		serial, \
		site_name, \
		stack_id, \
		status, \
		switch_type, \
		uplink_ports, \
		usage_int, \
		chassis_type, \
		commander_mac, \
		cpu_utilization, \
		default_gateway, \
		device_mode, \
		fan_speed, \
		max_power, \
		mem_free, \
		mem_total, \
		poe_consumption, \
		power_consumption, \
		temperature, \
		total_clients, \
		updated_at, \
		uptime, \
                customer_id)

#    print("------------------------")
    print(query)

    cursor.execute(query)
    cnx.commit()
   
# Update the device table with the site name
    query = "UPDATE central_tools.devices SET site_name = '{0}' WHERE serial = '{1}'".format(site_name,serial) 
    cursor.execute(query)
    cnx.commit()
     
cursor.close()
cnx.close()

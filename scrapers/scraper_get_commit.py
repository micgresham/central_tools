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

def get_DB_devices ():
    # set initial vars
    print ("Getting devices from database")
    cnx2 = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
    cursor2 = cnx2.cursor()

    query = "SELECT serial,site_name, NULL as last_refreshed FROM central_tools.devices"
    cursor2.execute(query)
    row_headers=[x[0] for x in cursor2.description] #this will extract row headers
    rv = cursor2.fetchall()
    dict_data=[]
    for result in rv:
      row_result = dict(zip(row_headers,result))
      dict_data.append(row_result)

#    print("====================")
#    print(dict_data)
#    print("====================")
    cursor2.close()
    cnx2.close()
    return dict_data

def get_device_commit_status (central, serial, loop_limit=0):
    # set initial vars
    print ("Getting commit state for " + serial)

    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "configuration/v1/auto_commit_state/devices"
    qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
    }

    qparams = {
      "device_serials": serial,
    }

#    print(api_function_url)
    response = requests.request("GET", api_function_url, headers=qheaders, params=qparams)
#    if "error" in response.json():
#      return "{'ERROR'}"
#    else:
#    print(response.json())
    if (response.status_code == 500):
       print(response.text)
       result_str = '{ "count": 0, "ports": [ { "admin_state": "","alignment": "","allowed_vlan": [],"duplex_mode": "-","has_poe": false,"intf_state_down_reason": "", "is_uplink": false,"macaddr": "", "mode": "", "mux": null, "oper_state": "Down", "phy_type": "None", "poe_state": "Down", "port": "0", "port_number": "", "power_consumption": "-", "rx_usage": 0, "speed": "0", "status": "Down", "trusted": false, "tx_usage": 0, "type": "Ethernet", "vlan": null, "vlan_mode": 1, "vsx_enabled": false }] }'
       error_str = '{ "Error": 1, "Error_text": "Internal server error"}'

       response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
       j_response_status = json.loads(response_status) 
       j_result = json.loads(result_str)
       j_error = json.loads(error_str)
       j_result.update(j_error)
       j_result.update(j_response_status)
       print(response.headers)

    elif (response.status_code == 200):
      error_str = '{ "Error": 0, "Error_text": "' '" }'
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_result = response.json()
      j_response_status = json.loads(response_status) 
      j_error = json.loads(error_str)
      j_result.update(j_error)
      j_result.update(j_response_status)

    elif (response.status_code == 401): # authentication timed out
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_result = json.loads(response_status) 

    elif (response.status_code == 404):
       print(response.text)
       result_str = '{ "count": 0, "ports": [ { "admin_state": "","alignment": "","allowed_vlan": [],"duplex_mode": "-","has_poe": false,"intf_state_down_reason": "", "is_uplink": false,"macaddr": "", "mode": "", "mux": null, "oper_state": "Down", "phy_type": "None", "poe_state": "Down", "port": "0", "port_number": "", "power_consumption": "-", "rx_usage": 0, "speed": "0", "status": "Down", "trusted": false, "tx_usage": 0, "type": "Ethernet", "vlan": null, "vlan_mode": 1, "vsx_enabled": false }] }'
       error_str = '{ "Error": 404, "Error_text": "No data found"}'

       response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
       j_response_status = json.loads(response_status) 
       j_result = json.loads(result_str)
       j_error = json.loads(error_str)
       j_result.update(j_error)
       j_result.update(j_response_status)
       print(response.headers)

    elif (response.status_code == 200):
      error_str = '{ "Error": 0, "Error_text": "' '" }'
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_result = response.json()
      j_response_status = json.loads(response_status) 
      j_error = json.loads(error_str)
      j_result.update(j_error)
      j_result.update(j_response_status)
    else:
      error_str = '{ "Error": 0, "Error_text": "' '" }'
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_result = response.json()
      j_response_status = json.loads(response_status) 
      j_error = json.loads(error_str)
      j_result.update(j_error)
      j_result.update(j_response_status)


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
customer_id = central_info['customer_id']
    
# get all device variables - this call takes some time
data_dict =[] 
data_dict = get_DB_devices()

cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
cursor = cnx.cursor()
if (len(data_dict) > 0):
  # iterate all the nested dictionaries with keys
  for i in data_dict:
    serial = i['serial']
    site_name = i['site_name']
    data2 = get_device_commit_status (central,serial)
    if data2['status_code'] == 401:
        print("=============================")
        print(" Reauthenticating to Central")
        print("=============================")
        central_info = test_central(userID)
        central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
        data2 = get_device_commit_status (central,serial)
    elif data2['status_code'] == 500:
        print("Got the dreaded Internal Server Error...sleeping 10 seconds and trying again")
        sleep(10)
        data2 = get_device_commit_status (central,serial)
  

    print("---------------")
    print(data2)
    print(data2['data'])
    if data2['data'] != []:
      if "auto_commit_state" in data2['data'][0]:
       auto_commit_state = data2['data'][0]['auto_commit_state']
      else:
         auto_commit_state = "Unknown"
    else:
      auto_commit_state = "Unknown"
     
    
    query = "UPDATE central_tools.devices SET auto_commit_state = '{0}' WHERE serial = '{1}'".format(auto_commit_state,serial) 
     

    print("------------------------")
    print(query)

    cursor.execute(query)
    cnx.commit()
     
cursor.close()
cnx.close()

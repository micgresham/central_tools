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

def get_DB_switches ():
    # set initial vars
    print ("Getting switches from database")
    cnx2 = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
    cursor2 = cnx2.cursor()

    query = "SELECT serial,site_name,name,stack_id,group_name, NULL as last_refreshed FROM central_tools.switches"
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

def get_switch_port_details (central, serial, loop_limit=0):
    # set initial vars
    print ("Getting switch port details for " + serial)

    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "monitoring/v1/switches/{0}/ports".format(serial)
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
data_dict = get_DB_switches()

cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
cursor = cnx.cursor()
if (len(data_dict) > 0):
  # iterate all the nested dictionaries with keys
  for i in data_dict:
    serial = i['serial']
    site_name = i['site_name']
    name = i['name']
    print(name)
    stack_id = i['stack_id']
    group_name = i['group_name']
    data2 = get_switch_port_details (central,serial)
    if data2['status_code'] == 401:
        print("=============================")
        print(" Reauthenticating to Central")
        print("=============================")
        central_info = test_central(userID)
        central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
        data2 = get_switch_port_details (central,serial)
    elif data2['status_code'] == 500:
        print("Got the dreaded Internal Server Error...sleeping 10 seconds and trying again")
        sleep(10)
        data2 = get_switch_port_details (central,serial)
  
#    print(data2)
    for j in data2['ports']:
#      print(j)
      admin_state = j['admin_state']
      if "alignment" in j:
        alignment = j['alignment']
      else:
        alignment = 'na'
      allowed_vlan = j['allowed_vlan']
      duplex_mode = j['duplex_mode']
      has_poe = sqlboolean(j['has_poe'])
      if "in_errors" in j:
        in_errors = j['in_errors']
      else:
        in_errors = 0
      if "out_errors" in j:
        out_errors = j['out_errors']
      else:
        out_errors = 0
      if "intf_state_down_reason" in j:
        intf_state_down_reason = j['intf_state_down_reason']
      else:
        intf_state_down_reason = 'na'
      is_uplink = sqlboolean(j['is_uplink'])
      macaddr = j['macaddr']
      mode = j['mode']
      if "mux" in j:
        mux = j['mux']
      else: 
        mux = 0
      oper_state = j['oper_state']
      phy_type = j['phy_type']
      poe_state = j['poe_state']
      port = j['port']
      port_number = j['port_number']

      if (j['power_consumption'] == None):
        power_consumption = 0
      elif (j['power_consumption'] == '-'):
        power_consumption = 0
      else:
        power_consumption = j['power_consumption']

      if "rx_usage" in j:
        rx_usage = j['rx_usage']
      else:
        rx_usage = j['rx_usage']
      speed = j['speed']
      status = j['status']
      trusted = sqlboolean(j['trusted'])
      if "tx_usage" in j: 
        tx_usage = j['tx_usage']
      else:
        tx_usage = 0
      type = j['type']
      if (j['vlan'] == None):
        vlan = 0
      else:
        vlan = j['vlan']
      if "vlan_mode" in data2['ports']:
        vlan_mode = j['vlan_mode']
      else:
        vlan_mode = 0
      if "vsx_enabled" in data2['ports']:
        vsx_enabled = sqlboolean(j['vsx_enabled'])
      else:
        vsx_enabled = 0
      
      queryU1 = "INSERT INTO central_tools.ports ( \
		admin_state, \
		allowed_vlan, \
		duplex_mode, \
		has_poe, \
		in_errors, \
		is_uplink, \
		macaddr, \
		mode, \
		mux, \
		oper_state, \
		out_errors, \
		phy_type, \
		poe_state, \
		port, \
		port_number, \
		power_consumption, \
		rx_usage, \
		speed, \
		status, \
		trusted, \
		tx_usage, \
		type, \
		vlan, \
                vlan_mode, \
                vsx_enabled, \
                serial, \
                alignment, \
                intf_state_down_reason, \
                name, \
                customer_id, \
		last_refreshed) \
      VALUES ('{0}','{1}','{2}',{3},{4},{5},'{6}','{7}','{8}','{9}',\
		{10},'{11}','{12}',{13},'{14}',{15},{16},'{17}','{18}',{19},{20}, \
		'{21}',{22},{23},'{24}','{25}','{26}','{27}','{28}','{29}',now())".format( \
		admin_state, \
		allowed_vlan, \
		duplex_mode, \
		has_poe, \
		in_errors, \
		is_uplink, \
		macaddr, \
		mode, \
		mux, \
		oper_state, \
		out_errors, \
		phy_type, \
		poe_state, \
		port, \
		port_number, \
		power_consumption, \
		rx_usage, \
		speed, \
		status, \
		trusted, \
		tx_usage, \
		type, \
		vlan, \
                vlan_mode, \
                vsx_enabled, \
                serial, \
                alignment, \
                intf_state_down_reason,
                name, \
                customer_id)
		

      query = queryU1 + " ON DUPLICATE KEY UPDATE  \
		admin_state = '{0}', \
		allowed_vlan = '{1}', \
		duplex_mode = '{2}', \
		has_poe = {3}, \
		in_errors = {4}, \
		is_uplink = {5}, \
		macaddr = '{6}', \
		mode = '{7}', \
		mux = '{8}', \
		oper_state = '{9}', \
		out_errors = '{10}', \
		phy_type = '{11}', \
		poe_state = '{12}', \
		port = {13}, \
		port_number = '{14}', \
		power_consumption = {15}, \
		rx_usage = {16}, \
		speed = '{17}', \
		status = '{18}', \
		trusted = {19}, \
		tx_usage = {20}, \
		type = '{21}', \
		vlan = {22}, \
                vlan_mode = {23}, \
                vsx_enabled = {24}, \
                serial = '{25}', \
                alignment = '{26}', \
                intf_state_down_reason = '{27}', \
                name = '{28}', \
                customer_id = '{29}', \
		last_refreshed = now()".format( \
		admin_state, \
		allowed_vlan, \
		duplex_mode, \
		has_poe, \
		in_errors, \
		is_uplink, \
		macaddr, \
		mode, \
		mux, \
		oper_state, \
		out_errors, \
		phy_type, \
		poe_state, \
		port, \
		port_number, \
		power_consumption, \
		rx_usage, \
		speed, \
		status, \
		trusted, \
		tx_usage, \
		type, \
		vlan, \
                vlan_mode, \
                vsx_enabled, \
                serial, \
                alignment, \
                intf_state_down_reason,
                name, \
                customer_id)

      print("------------------------")
      print(query)

      cursor.execute(query)
      cnx.commit()
     
cursor.close()
cnx.close()

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


def get_inventory (central,type, loop_limit=0):
    # set initial vars
    print ("Getting " + type + " inventory")

    # loop through call to get devices
    # stop when response is empty
    counter = 0
    need_more = True

    limit = 1000
    offset = 0

    s = requests.Session()

    retries = Retry(total=5,
                backoff_factor=1,
                status_forcelist=[ 502, 503, 504 ])

    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.mount('http://', HTTPAdapter(max_retries=retries))

    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "platform/device_inventory/v1/devices"
    qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
    }

    device_list = []

    while need_more:
        qparams = {
          "limit": limit,
          "offset": offset,
          "sku_type": type
        }

        response = s.request("GET", api_function_url, headers=qheaders, params=qparams)
        if response.json()['devices'] != []:
            device_list = device_list + response.json()['devices']
            offset += limit
        elif response.json()['devices'] == []:
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

def get_cfg_details_aps (serial):
    print ("Getting config details for " + serial)

    cnx2 = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
    cursor2 = cnx2.cursor()

    query = "SELECT templates.group_name, templates.template_name, templates.template_hash, aps.serial \
            FROM central_tools.aps\
            JOIN central_tools.templates ON aps.group_name = templates.group_name \
            WHERE aps.serial = '{0}'".format(serial); 

    cursor2.execute(query)
    row=cursor2.fetchone()
    data_dict = {}
    if (cursor2.rowcount < 1):
     data_dict['serial'] = serial 
     data_dict['template_name'] = "na"
     data_dict['template_hash'] = "na"
     data_dict['group_name'] = "na"

    else:
     data_dict['serial'] = row[3]
     data_dict['template_name'] = row[1]
     data_dict['template_hash'] = row[2]
     data_dict['group_name'] = row[0]

    cursor2.close()
    cnx2.close()
    
    return data_dict

def get_cfg_details_switch (serial):
    print ("Getting config details for " + serial)

    cnx2 = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
    cursor2 = cnx2.cursor()

    query = "SELECT templates.group_name, templates.template_name, templates.template_hash, switches.serial \
            FROM central_tools.switches \
            JOIN central_tools.templates ON switches.group_name = templates.group_name \
            WHERE switches.serial = '{0}'".format(serial); 

    cursor2.execute(query)
    row=cursor2.fetchone()
    data_dict = {}
    if (cursor2.rowcount < 1):
     data_dict['serial'] = serial 
     data_dict['template_name'] = "na"
     data_dict['template_hash'] = "na"
     data_dict['group_name'] = "na"

    else:
     data_dict['serial'] = row[3]
     data_dict['template_name'] = row[1]
     data_dict['template_hash'] = row[2]
     data_dict['group_name'] = row[0]

    cursor2.close()
    cnx2.close()
    
    return data_dict



parser = argparse.ArgumentParser()
parser.add_argument('--dev_type', \
                     default = 'ALL', \
                     help='Options are: switch, all_ap, all_controllers, vgw, cap, others. Default is ALL device types.')
parser.add_argument('--userID', \
                     default = 'scraper', \
                     help='Central Tools user ID to use for API access')
args = parser.parse_args()
dev_type = args.dev_type
userID = args.userID

print(dev_type)
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
if dev_type == "switch":
  data_dict = get_inventory(central,"switch")
if dev_type == "all_ap":
  data_dict = get_inventory(central,"all_ap") + data_dict
if dev_type == "all_controller":
  data_dict = get_inventory(central,"all_controller") + data_dict
if dev_type == "all_gateway":
  data_dict = get_inventory(central,"gateway") + data_dict
if dev_type == "all_vgw":
  data_dict = get_inventory(central,"vgw") + data_dict
if dev_type == "all_cap":
  data_dict = get_inventory(central,"cap") + data_dict
if dev_type == "all_others":
  data_dict = get_inventory(central,"others") + data_dict
if dev_type == "ALL":
  data_dict = get_inventory(central,"switch")
  data_dict = get_inventory(central,"all_ap") + data_dict
  data_dict = get_inventory(central,"all_controller") + data_dict
  data_dict = get_inventory(central,"gateway") + data_dict
  data_dict = get_inventory(central,"vgw") + data_dict
  data_dict = get_inventory(central,"cap") + data_dict
  data_dict = get_inventory(central,"others") + data_dict


cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
cursor = cnx.cursor()
if (len(data_dict) > 0):
  # iterate all the nested dictionaries with keys
  for i in data_dict:
    # display
    aruba_part_no = i['aruba_part_no']
    customer_id = i['customer_id']
    customer_name = i['customer_name']
    device_type = i['device_type']
    imei = i['imei']
    macaddr = i['macaddr']
    model = i['model']
    serial = i['serial']
    services = json.dumps(i['services'])
    tier_type = i['tier_type']

    if device_type == "switch":
      data2 = get_cfg_details_switch(serial)
      group_name = data2['group_name']
      template_name = data2['template_name']
      template_hash = data2['template_hash']
    elif device_type == "iap":
      data2 = get_cfg_details_aps(serial)
      group_name = data2['group_name']
      template_name = data2['template_name']
      template_hash = data2['template_hash']
    else:
      group_name = "na"
      template_name = "na"
      template_hash = "na"

    queryU1 = "INSERT INTO central_tools.devices ( \
  	aruba_part_no, \
  	customer_id, \
  	customer_name, \
  	device_type, \
  	imei, \
  	macaddr, \
  	model, \
  	serial, \
  	services, \
  	tier_type, \
  	group_name, \
  	template_name, \
  	template_hash, \
  	last_refreshed) \
        VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',\
	'{10}','{11}','{12}',now())".format( \
  	aruba_part_no, \
	customer_id, \
	customer_name, \
	device_type, \
	imei, \
	macaddr, \
	model, \
	serial, \
	services, \
        tier_type, \
	group_name, \
	template_name, \
	template_hash)

    query = queryU1 + " ON DUPLICATE KEY UPDATE  \
		aruba_part_no = '{0}', \
		customer_id = '{1}', \
		customer_name = '{2}', \
		device_type = '{3}', \
		imei = '{4}', \
		macaddr = '{5}', \
		model = '{6}', \
		serial = '{7}', \
		services = '{8}', \
                tier_type = '{9}', \
		group_name  = '{10}', \
		template_name = '{11}', \
		template_hash = '{12}', \
		last_refreshed = now()".format( \
		aruba_part_no, \
		customer_id, \
		customer_name, \
		device_type, \
		imei, \
		macaddr, \
		model, \
		serial, \
		services, \
                tier_type, \
		group_name, \
		template_name, \
		template_hash)

#    print("------------------------")
#    print(query)
    cursor.execute(query)
    cnx.commit()

cursor.close()
cnx.close()

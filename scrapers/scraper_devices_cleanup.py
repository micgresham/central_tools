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


def get_errored_inventory():
  print ("Getting errored inventory")
  central_info_func = {}

  cnx2 = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
  cursor2 = cnx2.cursor()

  query = "SELECT *, NULL as last_refreshed FROM central_tools.devices WHERE error = 1"
  cursor2.execute(query)
  row_headers=[x[0] for x in cursor2.description] #this will extract row headers
  rv = cursor2.fetchall()
  dict_data=[]
  for result in rv:
    row_result = dict(zip(row_headers,result))
    dict_data.append(row_result)

#  print(dict_data)
  cursor2.close()
  cnx2.close()
  return dict_data

def get_cfg_details (central, serial, loop_limit=0):
    # set initial vars
    print ("Getting config details for " + serial)

    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "configuration/v1/devices/{0}/config_details".format(serial)
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

    if (response.status_code == 400):
       result_str = '{"Device_serial": "na", "Device_type": "na", "Group": "na", "Configuration_error_status": false, "Override_status": false, "Template_name": "na", "Template_hash": "na", "Template_error_status": false,"Error": false, "Error_text": "na"}'
       error_str = '{ "Error": 1, "Error_text": "' + response.json()['description'] + '" }'
       response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
       j_response_status = json.loads(response_status) 
       j_result = json.loads(result_str)
       j_error = json.loads(error_str)
       j_result.update(j_error)
       j_result.update(j_response_status)
       print("===============")
       print(j_result)
       print("===============")

    elif (response.status_code == 500):
       print(response.text)
       j_response  = json.loads(response.text)

       result_str = '{"Device_serial": "na", "Device_type": "na", "Group": "na", "Configuration_error_status": false, "Override_status": false, "Template_name": "na", "Template_hash": "na", "Template_error_status": false,"Error": false, "Error_text": "na"}'
       error_str = '{ "Error": 1, "Error_text": "' + j_response['description'] + '-' + j_response['service_name'] + '-' + j_response['error_code'] + '"}'
       response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
       j_response_status = json.loads(response_status) 
       j_result = json.loads(result_str)
       j_error = json.loads(error_str)
       j_result.update(j_error)
       j_result.update(j_response_status)
       print(response.headers)

    elif (response.status_code == 200):
      regex1 = r"^--.*\W*Content-Disposition: form-data;\Wname=\"Summary\"\W*Content-Type.*\W*{"
      regex2 = r"}\W*--.*--\W*"
      regex3 = r"}\W*\*"

      clean_result = re.sub(regex1, "{", response.text, 0, re.IGNORECASE)
      clean_result = re.sub(regex2, "}", clean_result, 0, re.IGNORECASE)
      clean_result = re.sub(regex3, "", clean_result, 0, re.IGNORECASE)
      
      j_result = json.loads(clean_result)
      error_str = '{ "Error": 0, "Error_text": "' '" }'
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_response_status = json.loads(response_status) 
      j_error = json.loads(error_str)
      j_result.update(j_error)
      j_result.update(j_response_status)

    elif (response.status_code == 401): # authentication timed out
      response_status = '{ "status_code": ' + str(response.status_code)  + '}' 
      j_result = json.loads(response_status) 


    return j_result 



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
data_dict = get_errored_inventory()
#print(data_dict)
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
    services = i['services']
    tier_type = i['tier_type']
  
    data2 = get_cfg_details(central,serial)
    print(data2['status_code'])

    if data2['status_code'] == 401:
      print("=============================")
      print(" Reauthenticating to Central")
      print("=============================")
      central_info = test_central(userID)
      central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
      data2 = get_cfg_details(central,serial)

#    print(data2)
#    time.sleep(1)
    group_name = data2['Group']
    configuration_error_status = sqlboolean(data2['Configuration_error_status'])  
    override_status = sqlboolean(data2['Override_status'])
    template_name = data2['Template_name']
    template_hash = data2['Template_hash']
    template_error_status = sqlboolean(data2['Template_error_status'])
    error = data2['Error']
    error_text = data2['Error_text']
  

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
		configuration_error_status, \
		override_status, \
		template_name, \
		template_hash, \
		template_error_status, \
                error, \
                error_text, \
		last_refreshed) \
             VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',\
		'{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}',now())".format( \
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
		configuration_error_status, \
		override_status, \
		template_name, \
		template_hash, \
		template_error_status, \
                error, \
                error_text)

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
		configuration_error_status = '{11}', \
		override_status = '{12}', \
		template_name = '{13}', \
		template_hash = '{14}', \
		template_error_status = '{15}', \
                error = '{16}', \
                error_text = '{17}', \
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
		configuration_error_status, \
		override_status, \
		template_name, \
		template_hash, \
		template_error_status, \
                error, \
                error_text)

#    print("------------------------")
#    print(query)

    cursor.execute(query)
    cnx.commit()
     
cursor.close()
cnx.close()

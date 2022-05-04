#!/usr/bin/env python3

import datetime
import mysql.connector
import json
import requests
from pycentral.base import ArubaCentralBase
from pycentral.configuration import Templates
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


def get_db_groups():
    """ Get all groups from the database"""
    # set initial vars
    print ("Getting DB groups")
    group_list = []

# open the DB
    cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
    cursor = cnx.cursor()
    query = "SELECT group_name from central_tools.groups WHERE customer_id = '{0}'".format(central_info['customer_id'])
    cursor.execute(query)
    for (group_name) in cursor:
      group_list += group_name
 
# close the DB
    cursor.close()
    cnx.close()

    return group_list

def get_group_to_template (central, group_list):
    """Return group to template mapping."""
    print ("Getting Group to Template Mapping")
    # set initial vars
    t = Templates()
    group_to_template_dict = {}

    # loop over group list and get templates in each group - add to group_to_template_dict
    for gp in group_list:
        print (gp)
        response = t.get_template(central,group_name=gp)
        if response['code'] == 404:
            group_to_template_dict[gp]='none'
        elif response['code'] == 200:
            group_to_template_dict[gp]=response['msg']['data']
        else:
            group_to_template_dict[gp]='none'
    return group_to_template_dict 

central_info = test_central()
#print("--------------")
#print(central_info)
#print("--------------")

ssl_verify=True
# set Central data
central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
    
# get all device variables - this call takes some time
group_list = get_db_groups()
data_dict = get_group_to_template(central,group_list)

#print(data_dict)

cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
cursor = cnx.cursor()

# iterate all the nested dictionaries with keys

for i in data_dict:
  template_name = i
  device_type = ""
  group_name = ""
  model = ""
  template_hash = ""
  version = ""

  if (data_dict[i] != 'none'):
    device_type = data_dict[i][0]['device_type']
    group_name = data_dict[i][0]['group']
    model = data_dict[i][0]['model']
    template_hash = data_dict[i][0]['template_hash']
    version = data_dict[i][0]['version']

#  print(template_name)
#  print(device_type)
#  print(group_name)
#  print(model)
#  print(template_hash)
#  print(version)


  # display

    queryU1 = "INSERT INTO central_tools.templates ( \
                template_name, \
                customer_id, \
		device_type, \
		group_name, \
		model, \
		template_hash, \
		version, \
		last_refreshed) \
               VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}',now())".format( \
                template_name, \
		central_info['customer_id'], \
		device_type, \
		group_name, \
		model, \
		template_hash, \
		version)

    query = queryU1 + " ON DUPLICATE KEY UPDATE  \
                template_name = '{0}', \
		device_type = '{1}', \
		group_name = '{2}', \
		model = '{3}', \
		template_hash = '{4}', \
		version = '{5}', \
		last_refreshed = now()".format( \
                template_name, \
		device_type, \
		group_name, \
		model, \
		template_hash, \
		version)

#    print("------------------------")
#    print(query)

    cursor.execute(query)
    cnx.commit()
     
cursor.close()
cnx.close()

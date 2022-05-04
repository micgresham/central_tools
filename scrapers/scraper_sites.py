#!/usr/bin/env python3

import datetime
import mysql.connector
import json
import requests
from collections import ChainMap
from pycentral.base import ArubaCentralBase
from pycentral.monitoring import Sites
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

def get_sites (central,loop_limit=0):
    """ Return a full list of variables for all devices """
    print ("Getting Sites")
    # set initial vars
    limit = 500
    s = Sites()
    full_site_list = []

    # loop through call to get groups appending groups to full group list
    # stop when response is empty
    counter = 0
    need_more =  True

    while need_more:
        response = s.get_sites(central,offset=counter,limit=limit)
        if response['msg']['count'] != 0:
            full_site_list = full_site_list + response['msg']['sites']
        elif response['msg']['count'] == 0:
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

    return full_site_list

central_info = test_central()
#print("--------------")
#print(central_info)
#print("--------------")

ssl_verify=True
# set Central data
central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
    
# get all device variables - this call takes some time
data_list = get_sites(central)
#print(data_list)

cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
cursor = cnx.cursor()

# iterate all the nested dictionaries with keys
for i in data_list:
  # display
    site_id = i['site_id']
    site_name = sqlescape(i['site_name'])
    address = sqlescape(i['site_details']['address'])
    associated_device_count = i['associated_device_count']
    city = sqlescape(i['site_details']['city'])
    state = sqlescape(i['site_details']['state'])
    postal_code = sqlescape(i['site_details']['zipcode'])
    country = sqlescape(i['site_details']['country'])
    latitude = sqlescape(i['site_details']['latitude'])
    longitude = sqlescape(i['site_details']['longitude'])
    name = sqlescape(i['site_details']['name'])
    tags = sqlescape(i['tags'])   

    queryU1 = "INSERT INTO central_tools.sites (customer_id,site_id,site_name, \
                address,associated_device_count,city, \
                state,postal_code,country,latitude, \
                longitude,name,tags,last_refreshed) \
                VALUES ('{0}','{1}','{2}','{3}',{4},'{5}','{6}','{7}','{8}','{9}', \
                '{10}','{11}','{12}',now())".format(central_info['customer_id'], \
                site_id,site_name,address,associated_device_count,city,state,postal_code, \
                country,latitude,longitude,name,tags)
    query = queryU1 + " ON DUPLICATE KEY UPDATE  site_name = '{0}', \
             address = '{1}',  \
             associated_device_count = {2}, \
             city = '{3}', \
             state = '{4}', \
             postal_code = '{5}', \
             country = '{6}', \
             latitude = '{7}', \
             longitude = '{8}', \
             name = '{9}', \
             tags = '{10}', \
             last_refreshed = now()".format( \
             site_name, \
             address, \
             associated_device_count, \
             city, \
             state, \
             postal_code, \
             country, \
             latitude, \
             longitude, \
             name, \
             tags)
#    print("------------------------")
#    print(query)

    cursor.execute(query)
    cnx.commit()
     
cursor.close()
cnx.close()

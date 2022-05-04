#!/usr/bin/env python3

import datetime
import mysql.connector
import json
import requests
from pycentral.base import ArubaCentralBase
from pycentral.configuration import Variables
from central_test_mysql import test_central

def get_all_variables (central,loop_limit=0):
    """ Return a full list of variables for all devices """
    print ("Getting Variables - Will Take Some time")
    # set initial vars
    limit = 20
    v = Variables()
    full_variable_dict = {}

    # loop through call to get groups appending groups to full group list
    # stop when response is empty
    counter = 0
    need_more =  True

    while need_more:
        response = v.get_all_template_variables(central,offset=counter,limit=limit)
        if response['msg'] != {}:
            full_variable_dict.update(response['msg'])
        elif response['msg'] == {}:
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
    return full_variable_dict

central_info = test_central()
#print("--------------")
#print(central_info)
#print("--------------")

ssl_verify=True
# set Central data
central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
    
# get all device variables - this call takes some time
data_dict = get_all_variables (central)
print(data_dict)
cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
cursor = cnx.cursor()

# iterate all the nested dictionaries with keys
for i in data_dict:
  # display
    serial = i 
    for j in data_dict[i]:
      variable_name = j
      value = data_dict[i][j]

      queryU1 = "INSERT INTO central_tools.variables (variable_name,customer_id,value,serial,last_refreshed) VALUES ('{0}','{1}','{2}','{3}',now())".format(variable_name,central_info['customer_id'],value,serial)
      query = queryU1 + " ON DUPLICATE KEY UPDATE  value = '{0}', last_refreshed = now()".format(value)

      print(query)

      cursor.execute(query)
      cnx.commit()
      
# remove any old variables over 7 days old
#      query = "DELETE FROM central_tools.variables WHERE last_refreshed < now() - INTERVAL 7 day"
#      cursor.execute(query)
#      cnx.commit()
       
cursor.close()
cnx.close()

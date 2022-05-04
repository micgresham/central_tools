#!/usr/bin/env python3

import datetime
import mysql.connector
import json
import requests
import re

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


def get_cfg_details (central, serial):
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

    print(api_function_url)
    response = requests.request("GET", api_function_url, headers=qheaders, params=qparams)
#    if "error" in response.json():
#      return "{'ERROR'}"
#    else:

    if (response.status_code != 500):
      print("PLAIN----------")
      print(response.text)
      print("----------")

      regex1 = r"^--.*\W*Content-Disposition: form-data;\Wname=\"Summary\"\W*Content-Type.*\W*{"
      regex2 = r"}\W*--.*--\W*"
      regex3 = r"}\W*\*"

      clean_result = re.sub(regex1, "{", response.text, 0, re.IGNORECASE)
      clean_result = re.sub(regex2, "}", clean_result, 0, re.IGNORECASE)
      clean_result = re.sub(regex3, "", clean_result, 0, re.IGNORECASE)

      print("CLEAN----------")
      print(clean_result)
      print("JSON----------")
      j_result = json.loads(clean_result)
      print(j_result)
      for i in j_result:
       print(i)


    return response



central_info = test_central()
#print("--------------")
#print(central_info)
#print("--------------")

ssl_verify=True
# set Central data
central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
    
data2 = get_cfg_details(central,"CNN6KD5FW")
print(data2)


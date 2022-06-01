#!/usr/bin/env python3

import datetime
import mysql.connector
import json
import requests
from pycentral.base import ArubaCentralBase



def test_central(scraperID = "scraper"):

  central_info_func = {}

  cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
  cursor = cnx.cursor()

  query = "SELECT id,username FROM central_tools_admin.auth_user where username = '{0}'".format(scraperID)
  cursor.execute(query)
  row=cursor.fetchone()
  user_id=row[0]

  query = "select * from central_tools_admin.home_profile where user_id = '{0}'".format(user_id)
  cursor.execute(query)
  row=cursor.fetchone()

  base_url = row[3]
  central_info_func['base_url'] = base_url
  customer_id = row[4]
  central_info_func['customer_id'] = customer_id
  client_id = row[5]
  client_secret = row[6]
  access_token = row[7]
  central_info_func['token'] = {}
  central_info_func['token']['access_token'] = access_token

  refresh_token = row[8]

  oath2_url = base_url + "/oauth2/token"
  api_test_url = base_url + "/configuration/v2/groups"

  #is out token valid?
  qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
      "limit": "1"
  }

  qparams = {
      "limit": 1,
      "offset": 0
  
  }

  print("Validating ACCESS TOKEN")
  response = requests.request("GET", api_test_url, headers=qheaders, params=qparams)

  if "error" in response.json():

    print("ACCESS TOKEN is INVALID or EXPIRED.  Refreshing tokens...")

    #refresh the token
    qparams = {
        "grant_type":"refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
  
    response = requests.request("POST", oath2_url, params=qparams)
 
    print(response.text.encode('utf8'))

    if "error" in response.json():

      print("UNABLE to refresh ACCESS TOKEN. REFRESH TOKEN, CLIENT ID or CLIENT SECRET INVALID")
      return({})

    else:
      # extract the new refresh oken from the response
      refresh_token = response.json()['refresh_token']
      access_token = response.json()['access_token']
      central_info_func['token']['access_token'] = access_token
      expires_in = response.json()['expires_in']
      central_info_func['expires_in'] = expires_in
  
      query = "UPDATE central_tools_admin.home_profile set central_token = '{0}',central_refresh_token = '{1}' WHERE user_id = '{2}'".format(access_token,refresh_token,user_id)
      cursor.execute(query)
      cnx.commit()
    
  else:
    print("ACCESS TOKEN is vlaid.  No action required.")
  
  cursor.close()
  cnx.close()
  return central_info_func
  
print(test_central())
 


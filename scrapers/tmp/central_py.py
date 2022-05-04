#!/usr/bin/env python3

import requests
import json
import getpass
import logging
import time
import sys
import re

"""
Base module used for completing common tasks used in the Aruba Central Environment.

Once Fed token generation information it will refresh (or regenerate) Bearer token.
"""
__author__ = "Jay McNealy"
__copyright__ = "None"
__credits__ = ["Jay McNealy"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "Jay McNealy"
__email__ = "justin.mcnealy@hpe.com"
__status__ = "Testing"

'''
Change log
            1.0.0 Initial module creation with a token generation class and a basic runner class with Get function
            1.1.0 Adding module documentation 

'''


# class Helper:
#     def __init__(self):
#         '''The helper class is initialized'''
#
#     def print_help(self):
#         '''Module used to assist interactions with Aruba Central API calls'''
#         #print('Module used to assist interactions with Aruba Central API calls')


# Class used to generate a new token.
class TokenGen:

    # Initialize function with required kwargs.
    def __init__(self, **kwargs):
        self.tokenInfo = {}
        if "access_token" in kwargs:
            self.tokenInfo["access_token"] = kwargs["access_token"]

        if "refresh_token" in kwargs:
            self.tokenInfo["refresh_token"] = kwargs["refresh_token"]

        if "uri" in kwargs:
            self.tokenInfo["uri"] = kwargs["uri"]

        if "customer_id" in kwargs:
            self.tokenInfo["customer_id"] = kwargs["customer_id"]

        if "client_id" in kwargs:
            self.tokenInfo["client_id"] = kwargs["client_id"]

        if "client_secret" in kwargs:
            self.tokenInfo["client_secret"] = kwargs["client_secret"]

    # Decorator used to time API calls
    def timer(func):
        def wrapper(self, *args, **kwargs):
            start = time.time()
            print('starting')
            rv = func(self, *args, **kwargs)
            total = time.time() - start
            logger.info(" took {} to return".format(total))
            return rv

        return wrapper

    # Basic Testing Function
    @staticmethod
    def test():
        now = time.asctime(time.localtime(time.time()))
        # print (self.tokenInfo)
        print(now)

    # Function to try a token refresh, if failed the script will attempt a full generation
    def gentok(self):
        if "refresh_token" in self.tokenInfo:
            refresh_test = self.refresh()
            logger.info('[*] Attempting Token Refresh')
            if 'ERROR' in refresh_test:
                logger.warning('[*] Refresh failed: attempting full token generation')
                fun_login, cookies = self.apilogin()
                logger.info('[*] Login Successful ')
                logger.info('[*] Cookies = {}'.format(cookies))
                fun_getcode = self.get_code(cookies['csrftoken'], cookies['session'])
                logger.info('[*] Get Code Successful')
                fun_getcode = json.loads(fun_getcode)
                token = self.get_tokn(cookies['csrftoken'], cookies['session'], fun_getcode['auth_code'])
                logger.info('[*] Full token generation Successful')
                return token
            else:
                logger.info('[*] Token Refresh Successful')
                return refresh_test
        elif "customer_id" in self.tokenInfo and \
                "client_id" in self.tokenInfo and \
                "client_secret" in self.tokenInfo and \
                "uri" in self.tokenInfo:
            logger.info('[*] No refresh token data provided. running full generation')
            fun_login, cookies = self.apilogin()
            logger.info('[*] Login Successful ')
            # logger.info(fun_login)
            logger.info('[*] Cookies = {}'.format(cookies))
            fun_getcode = self.get_code(csrf=cookies['csrftoken'], sess=cookies['session'])
            logger.info('[*] Get Code Successful')
            fun_getcode = json.loads(fun_getcode)
            token = self.get_tokn(cookies['csrftoken'], cookies['session'], fun_getcode['auth_code'])
            logger.info('[*] Full token generation Successful')
            return token
        else:
            print(
                "ERROR: required information for token Generation is, at minimum, Customer ID, OAuth client ID, "
                "OAuth Client secret and the URL for Central.")
            sys.exit()

    @timer
    # API call function to login to APC and get cookies required
    def apilogin(self):
        """Will prompt for Username and Password and login to Central

            Returns response text and cookies

            RReturns ERROR 9 If login fails
        """
        username = input('Username: ')
        password = getpass.getpass('password: ')

        url = self.tokenInfo["uri"] + "/oauth2/authorize/central/api/login?client_id=" + self.tokenInfo["client_id"]
        logger.info('[*] apilogin url: {}'.format(url))
        payload = "{\"username\": \"%s\",\r\n\"password\": \"%s\"}" % (username, password)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        f = (requests.utils.dict_from_cookiejar(response.cookies))
        logger.debug('[*] response code for apilogin = %s' % response.status_code)
        if response.status_code == 200:
            return response.text, f
        else:
            logger.error("[!] Error: apilogin failed with error code %s" % response.status_code)
            logger.info('[!] Error: Response code: '.format(response.text))
            logger.warning("[!] ERROR 9")
            sys.exit()

    @timer
    # API function to get Auth code from APC *note Customer Id must match with Client id used in logi
    def get_code(self, csrf, sess):
        """
        Takes cookies from login and gets the code required tro generate a OAuth Bearer token
        :param csrf: CSRF cookie from login call
        :param sess: Session key from login call
        :return: response text which contains the code (STR)
        """
        url = self.tokenInfo["uri"] + "/oauth2/authorize/central/api?client_id=" + self.tokenInfo[
            "client_id"] + "&response_type=code&scope=all"
        logger.info('[*] getcode url: {}'.format(url))
        # querystring = {"client_id":self.tokenInfo["client_id"],"response_type":"code","scope":"all"}

        payload = "{\"customer_id\": \"%s\"}" % self.tokenInfo["customer_id"]
        logger.info('[*] apilogin payload: {}'.format(payload))
        headers = {
            'Content-Type': "application/json",
            'X-CSRF-TOKEN': "%s" % csrf,
            'Cookie': "session=%s" % sess,
            'Cache-Control': "no-cache",
        }
        # print (headers)
        response = requests.request("POST", url, data=payload, headers=headers)
        # return
        logger.debug('[*] response code for Get_Code = %s' % response.status_code)
        if response.status_code == 200:
            return response.text
        else:
            logger.error("[!] Error: getcode failed with error code %s" % response.status_code)
            logger.info('[!] Error: Response code: '.format(response.text))
            logger.warning("[!] ERROR 10")
            sys.exit()

    @timer
    # Final step is to generate the token. API If customer ID did not match Client id an error would be seen here
    def get_tokn(self, csrf, sess, code):
        """
        Uses login cookies and code to generate a Berarer token
        :param csrf: CSRF cookie from login call
        :param sess: Session key from login call
        :param code: Code recived by GetCode call
        :return: api return text containing Bearer token (STR)
        """
        url = self.tokenInfo["uri"] + "/oauth2/token?client_id=" + self.tokenInfo["client_id"] + "&client_secret=" + \
              self.tokenInfo["client_secret"] + "&grant_type=authorization_code&code=" + code
        logger.info('[*] Get_Tokn url: {}'.format(url))

        headers = {
            'Content-Type': "application/json",
            'X-CSRF-TOKEN': "%s" % csrf,
            'Cookie': "session=%s" % sess,
            'Cache-Control': "no-cache",
        }

        response = requests.request("POST", url, headers=headers)
        logger.debug('[*] response code for Get_tokn = %s' % response.status_code)
        if response.status_code == 200:
            return response.text
        else:
            logger.error("[!] Error: strt_trblshooting for %s failed with error code %s"%(response.status_code))
            logger.warning('[!] Error: Response code: '.format(response.text))
            logger.warning("[!] ERROR 11")
            sys.exit()

    @timer
    # API Attempt to refresh token
    def refresh(self):

        url = self.tokenInfo["uri"] + "/oauth2/token"
        querystring = {"grant_type": "refresh_token", "client_id": self.tokenInfo["client_id"],
                       "client_secret": self.tokenInfo["client_secret"],
                       "refresh_token": self.tokenInfo["refresh_token"]}

        headers = {
        }
        response = requests.request("POST", url, headers=headers, params=querystring)
        logger.info('[*] response code for refresh_tok = %s' % response.status_code)
        if response.status_code == 200:
            return response.text
        else:
            logger.error("[*] Error: strt_trblshooting for failed with error code %s"%(response.status_code))
            logger.warning('[!] Failed to refresh with error: ' + response.text)
            return '[!] ERROR 12'


# Class used to run various API calls * Requires an active Bearer Token
class Runner:
    """
    Class used to run API calls.
    """
    def __init__(self, bearertokn, uri):
        self.bearertokn = bearertokn
        self.uri = uri

    # Method to run get type API calls
    def get(self, url):
        """
        Method to run Get calls to Central
        :param url: Get URL address
        :return: API Response text (Str)
        """

        headers = {
            'Authorization': 'Bearer ' + self.bearertokn,
            'Content-Type':'application/json',
        }
        # print (headers)
        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            logger.info(response.status_code)
            logger.info(response.status_code)
            return response.text
        else:
            logger.error("[*] Error: Get call failed with error code %s" % (response.status_code))
            logger.warning('[!] Failed to run Get API with error: ' + response.text)
            return '[!] ERROR 13'

    # method to run all 3 API calls required to run a Switch troubleshooting API;
    # requires Serial of device and the command number for troubleshooting cmd.
    def sw_tshoot(self, serial, cmd):
        """
        Method to run Troubleshooting APIs  for Switches in Central
        :param serial: Serial of the Switch (STR)
        :param cmd: Troubleshooting cmd number (Int)
        :return: return text from API harvesting troublshooting data.
        """
        print('init tshoot')
        trouble_sessid, serial = self.sw_starttbl(serial, cmd)
        logger.info('(18018) Trouble session ID: {}'.format(trouble_sessid))
        if trouble_sessid == 'ERROR':
            print('Troubleshooting cmd Failed')
            sys.exit()
        tbdata = self.sw_gettrouble(serial, trouble_sessid)
        tblstatus = tbdata['status']
        # print (tblstatus)
        while tblstatus == 'RUNNING':
            time.sleep(2)
            print(tblstatus)
            tbdata = self.sw_gettrouble(serial, trouble_sessid)
            tblstatus = tbdata['status']
        clear = self.sw_clr_trblshooting(serial, trouble_sessid)
        print(clear)
        return tbdata

    # Method to initiate Switch Troubleshooting API call; requires Serial of device and the command number for
    # troubleshooting cmd.
    def sw_starttbl(self, serial, cmd):
        url = self.uri + "/troubleshooting/v1/devices/" + serial
        # print (url)
        payload = "{\n  \"device_type\": \"SWITCH\",\n  \"commands\": [\n    {\n      \"command_id\": %s,\n      \"arguments\": [\n        {\n          \"name\": \"string\",\n          \"value\": \"string\"\n        }\n      ]\n    }\n  ]\n}" % cmd
        # print (payload)
        headers = {
            'Authorization': "Bearer %s" % self.bearertokn,
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        # print (response.text)
        tblstrt = json.loads(response.text)
        logger.info('(18011)strt_trblshooting : %s' % response.status_code)
        if response.status_code == 200:
            print('Done sw strt')
            return tblstrt["session_id"], serial
        elif response.status_code == 400 and 'commander' in tblstrt['description']:
            logger.error("(18012)Error: Non-commander Stack member Trying to determine cmdr and Run. ")
            cmdr_srch = re.search(r'commander \w+', tblstrt['description'])
            if cmdr_srch:
                cmdr = cmdr_srch.group()
                cmdr = cmdr.split()
                serial = cmdr[-1]
                url = self.uri + "/troubleshooting/v1/devices/" + serial
                response = requests.request("POST", url, data=payload, headers=headers)
                tblstrt = json.loads(response.text)
                if response.status_code == 200:
                    logger.info('(18017) stacked switch cmdr found')
                    logger.info('(18016)CMDR found {}. response: {}'.format(cmdr[-1], tblstrt))
                    return tblstrt["session_id"], serial
                else:
                    logger.info('(18013)strt_trblshooting code: %s' % response.status_code)
                    logger.info('(18014)strt_trblshooting text: %s' % response.text)
                    return "ERROR", serial
            else:
                # print ('failed re(1)')
                logger.info('(18015)RE search for commander failed')
                return "ERROR", serial

        else:
            logger.error(
                "(18011)Error: strt_trblshooting for %s failed with error code %s" % (serial, response.status_code))
            return "ERROR", serial

    # Method to run API call that gathers output of switch troubleshooting call; requires Serial of device and the command
    # number for troubleshooting cmd.
    def sw_gettrouble(self, serial, sess_id):

        url = self.uri + "/troubleshooting/v1/devices/" + serial

        querystring = {"session_id": sess_id}

        # payload = "{\n  \"device_type\": \"SWITCH\",\n  \"commands\": [\n    {\n      \"command_id\": 90,\n      \"arguments\": [\n        {\n          \"name\": \"string\",\n          \"value\": \"string\"\n        }\n      ]\n    }\n  ]\n}"
        headers = {
            'Authorization': "Bearer %s" % self.bearertokn,
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",

        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        trblsh = json.loads(response.text)
        # print (trblsh)
        logger.info('(18012)get_trblshooting : %s' % response.status_code)
        # logger.info( '(18019){}'.format (trblsh))
        return trblsh

    # Method to clean up the troubleshooting call; requires Serial of device and the command number for
    # troubleshooting cmd.
    def sw_clr_trblshooting(self, serial, sess_id):
        url = self.uri + "/troubleshooting/v1/devices/" + serial

        querystring = {"session_id": sess_id}

        headers = {
            'Authorization': "Bearer %s" % self.bearertokn,
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
            'Postman-Token': "c417eca1-26ea-40e0-a258-dfe0e40f92e8"
        }

        response = requests.request("DELETE", url, headers=headers, params=querystring)

        return response.text


logger = logging.getLogger('Central_py_module')
# help(Helper)

# help(Helper.print_help)



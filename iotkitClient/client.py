"""@package Client
Methods for IoT Analytics Cloud connections
"""
from utils import *
import globals
import json
import requests

## Connection object for user session
#
# @param host
# @param username
# @param password
# @param proxies

class Client: 
    proxies     = ''
    #base_url    = ''
    user_token  = ''
    user_id     = ''
    
    def __init__(self, username, password, proxies=None):
        if not username or not password:
            raise ValueError("Invalid parameter: Client(username, password, [proxies])")
        # try:
        self.proxies = proxies
        #self.base_url = "https://{0}{1}".format(globals.host, globals.api_root)
        url = "{0}/auth/token".format(globals.base_url)    
        headers = {'content-type': 'application/json'}
        payload = {"username": username, "password": password}
        data = json.dumps(payload) 
        resp = requests.post(url, data=data, headers=headers, proxies=proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        self.user_token = js['token']           
        
        # get my user_id (uid) within the Intel IoT Analytics Platform
        js = self.get_user_tokeninfo()
        self.user_id = js["payload"]["sub"]
        
        # except Exception, err:
            # raise RuntimeError('Auth ERROR: %s\n' % str(err))
        
    # given a user token, get the user_id
    def get_user_tokeninfo(self):        
        url = "{0}/auth/tokenInfo".format(globals.base_url)
        headers = {'content-type': 'application/json'}
        resp = requests.get(url, headers=get_auth_headers(self.user_token), proxies=self.proxies, verify=globals.g_verify)        
        check(resp, 200)
        js = resp.json()
        return js  

    # Health API
    def getVersion(self):
        url = "{0}/health".format(globals.base_url)
        headers = {'content-type': 'application/json'}
        resp = requests.get(url, headers=headers, proxies=self.proxies, verify=globals.g_verify)        
        check(resp, 200)
        js = resp.json()
        return js
        
    # static method
    @staticmethod
    def getVersion(proxies=None):
        url = "{0}/health".format(globals.base_url)
        headers = {'content-type': 'application/json'}
        resp = requests.get(url, headers=headers, proxies=proxies, verify=globals.g_verify)        
        check(resp, 200)
        js = resp.json()
        return js
        
    # Re-initialize to get new token (use after creating a new account)
    def reinit(self, username, password):    
        if not username or not password:
            raise ValueError("Invalid parameter: reinit(username, password)")    
        url = "{0}/auth/token".format(globals.base_url)    
        headers = {'content-type': 'application/json'}
        payload = {"username": username, "password": password}
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=headers, proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        self.user_token = js['token'] 
        

"""@package Client
Methods for IoT Analytics Cloud connections
"""
from utils import *
from globals import *
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
    base_url    = ''
    user_token  = ''
    user_id     = ''
    
    def __init__(self, host, username, password, proxies=None):
        if not host or not username or not password:
            raise ValueError("Invalid parameter: Client(host, username, password, [proxies])")
        
        self.proxies = proxies
        api_root = "/v1/api"
        self.base_url = "https://{0}{1}".format(host, api_root)
        url = "{0}/auth/token".format(self.base_url)    
        headers = {'content-type': 'application/json'}
        payload = {"username": username, "password": password}
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=headers, proxies=self.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        self.user_token = js['token'] 
        #print "User Token:", self.user_token        
        
        # get my user_id (uid) within the Intel IoT Analytics Platform
        js = self.get_user_tokeninfo()
        self.user_id = js["payload"]["sub"]
            
    # given a user token, get the user_id
    def get_user_tokeninfo(self):        
        url = "{0}/auth/tokenInfo".format(self.base_url)
        resp = requests.get(url, headers=get_user_headers(self.user_token), proxies=self.proxies, verify=g_verify)        
        check(resp, 200)
        js = resp.json()
        return js    

    # Health API
    def getVersion(self):
        url = "{0}/health".format(self.base_url)
        resp = requests.get(url, headers=get_user_headers(self.user_token), proxies=self.proxies, verify=g_verify)        
        check(resp, 200)
        js = resp.json()
        return js
        
    # Re-initialize to get new token (use after creating a new account)
    def reinit(self, username, password):        
        url = "{0}/auth/token".format(self.base_url)    
        headers = {'content-type': 'application/json'}
        payload = {"username": username, "password": password}
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=headers, proxies=self.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        self.user_token = js['token'] 
        

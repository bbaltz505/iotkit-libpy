"""@package User
Methods for IoT Analytics user management
"""
from globals import *
from utils import *
import requests
import json

class User:
    id     = None
    client = None
    
    def __init__(self, client):
        self.client = client
        js = client.get_user_tokeninfo()
        if js["payload"]["sub"]:
            self.id = js["payload"]["sub"]
        
    def setUser(self, user_id=None):
        if user_id == None:
            user_id = self.id
            
        # Get the user's info
        url = "{0}/users/{1}".format(self.client.base_url, user_id)
        resp = requests.get(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        return js
        
    def update(self, user_id, user_info):
        if user_id and user_info:
            # given a user_id, get the user's info
            url = "{0}/users/{1}".format(self.client.base_url, user_id)
            data = json.dumps(user_info)
            resp = requests.put(url, data=data, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
            check(resp, 200)
        else:
            raise ValueError("No user ID given.")
        return None
        
    def findAccounts(self, account_name, firstAccountOnly=True):
        accounts = []
        if account_name:
            js = self.setUser()
            if js["accounts"]:
                for account, value in js["accounts"].items():
                    if value["name"] == account_name:
                        accounts.append(account)
        else:
            raise ValueError("No account_name given.")
            
        if firstAccountOnly:
            return accounts[0]
        return accounts
from globals import *
from utils import *
import requests
import json

class User:
    id     = None
    client = None
    
    def __init__(self, client):
        self.client = client
        
    def get(self, user_id):
        if user_id:
            # given a user_id, get the user's info
            url = "{0}/users/{1}".format(self.client.base_url, user_id)
            resp = requests.get(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
            check(resp, 200)
            js = resp.json()
            if js:
                self.id = js["id"]
                return js
            raise ValueError("Empty user record")
        else:
            raise ValueError("No user ID given.")
        return None
        
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
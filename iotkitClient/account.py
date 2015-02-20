"""@package Account
Methods for IoT Analytics account management
"""
import globals
from utils import *
import requests
import json

class Account:
    #id     = None
    client = None
    
    def __init__(self, client):
        self.client = client
        
    def create(self, account_name):
        if account_name:
            url = "{0}/accounts".format(globals.base_url)
            payload = {"name": account_name}
            data = json.dumps(payload)
            resp = requests.post(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 201)
            js = resp.json()
            #self.id = js["id"]
            self.updateProperties(js) # save account properties
            return js
        else:
            raise ValueError("No account name given.")
        
    def getAccount(self, account_name, account_id=None):
        if account_name:
            # given a user_id, get the account_id of the associated account with account_name
            # if there are multiple accounts with the same name, return one of them
            url = "{0}/users/{1}".format(globals.base_url, self.client.user_id)
            resp = requests.get(url, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            if 'accounts' in js:
                accounts = js["accounts"]
                for k, v in accounts.iteritems():
                    if 'name' in v and v["name"] == account_name:
                        # if account_id is given, verify its value also
                        if account_id and account_id == k or not account_id:
                            self.id = k
                            return self.id
            msg =  "Account name {0} not found.".format(account_name)
            msg += "Available accounts are: {0}".format([v["name"] for k, v in accounts.iteritems()]) 
            raise ValueError(msg)
        else:
            raise ValueError("No account name given.")
        
    def getInfo(self):
        url = "{0}/accounts/{1}".format(globals.base_url, self.id)
        resp = requests.get(url, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        self.updateProperties(js) # save account properties
        return js
        
    def update(self, acct_info):
        data = json.dumps(acct_info)
        if acct_info:
            url = "{0}/accounts/{1}".format(globals.base_url, self.id)
            resp = requests.put(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            self.updateProperties(js) # save account properties
            return js
        else:
            raise ValueError("Invalid account info given.")
            
    def getActivationCode(self):
        url = "{0}/accounts/{1}/activationcode".format(globals.base_url, self.id)
        resp = requests.get(url, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js["activationCode"]
    
    def renewActivationCode(self):
        url = "{0}/accounts/{1}/activationcode/refresh".format(globals.base_url, self.id)
        resp = requests.put(url, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js["activationCode"] 
        
    def delete(self, account_id):
        if account_id:
            url = "{0}/accounts/{1}".format(globals.base_url, account_id)
            resp = requests.delete(url, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 204)
        else:
            raise ValueError("Invalid account ID.")
        
    def getAccountUser(self):
        url = "{0}/accounts/{1}/users".format(globals.base_url, self.id)
        resp = requests.get(url, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js
        
    def addUser(self, user_info, user_id):
        
        url = "{0}/accounts/{1}/users/{2}".format(globals.base_url, self.id, user_id)
        data = json.dumps(payload)
        #print url, data
        resp = requests.put(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    def load_cert(self, file):
        token = None
        json_data=open(file).read()
        data = json.loads(json_data)
        if data["accountId"] == self.id:
            token = data["deviceToken"]
        return token
        
    def getData(self, time0, time1, devices, components, csv=None):
        url = "{0}/accounts/{1}/data/search".format(globals.base_url, self.id)
        if csv:
            url += "?output=csv"
        payload = {
          "from": time0,
          #"to": time1,
          "targetFilter": {
            "deviceList": devices
          },
          "metrics": [
            # {
              # "id": "<component_id>",
              # "op": "none" // currently it's the only value supported
            # }
          ]
        } 
        if time1:
            payload["to"] = time1
        for c in components:
            payload["metrics"].append({"id": c, "op": "none"})
        payload["targetFilter"]["deviceList"] = devices
        data = json.dumps(payload)
        #print data
        resp = requests.post(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        if csv:
            return resp.text
        else:
            js = resp.json()
            return js["series"]
            
    def advancedQuery(self, payload):
        url = "{0}/accounts/{1}/data/search/advanced".format(globals.base_url, self.id)
        
        data = json.dumps(payload)
        #print url, data
        resp = requests.post(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js
        
    def dataReport(self, payload, output=None):
        url = "{0}/accounts/{1}/data/report".format(globals.base_url, self.id)
        
        data = json.dumps(payload)
        #print url, data
        resp = requests.post(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js    

    def updateProperties(self, var):
        for key, value in var.items():
            setattr(self, key, value)
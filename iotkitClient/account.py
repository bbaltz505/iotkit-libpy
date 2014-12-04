from globals import *
from utils import *
import requests
import json

class Account:
    id     = None
    client = None
    
    def __init__(self, client):
        self.client = client
        
    def create(self, account_name):
        if account_name:
            url = "{0}/accounts".format(self.client.base_url)
            payload = {"name": account_name}
            data = json.dumps(payload)
            resp = requests.post(url, data=data, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
            check(resp, 201)
            js = resp.json()
            self.id = js["id"]
            return js
        else:
            raise ValueError("No account name given.")
        
    def setAccount(self, account_name, account_id=None):
        if account_name:
            # given a user_id, get the account_id of the associated account with account_name
            # if there are multiple accounts with the same name, return one of them
            url = "{0}/users/{1}".format(self.client.base_url, self.client.user_id)
            resp = requests.get(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
            check(resp, 200)
            js = resp.json()
            if 'accounts' in js:
                accounts = js["accounts"]
                for k, v in accounts.iteritems():
                    if 'name' in v and v["name"] == account_name:
                        print account_id, k
                        # if account_id is given, verify its value also
                        if account_id and account_id == k or not account_id:
                            self.id = k
                            return self.id
            print "Account name {0} not found.".format(account_name)
            print "Available accounts are: {0}".format([v["name"] for k, v in accounts.iteritems()]) 
        else:
            raise ValueError("No account name given.")
        
    def getAccountInfo(self):
        url = "{0}/accounts/{1}".format(self.client.base_url, self.id)
        resp = requests.get(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        return js
        
    def update(self):
        pass
        
    def getActivationCode(self):
        url = "{0}/accounts/{1}/activationcode".format(self.client.base_url, self.id)
        resp = requests.get(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        return js["activationCode"]
    
    def renewActivationCode(self):
        url = "{0}/accounts/{1}/activationcode/refresh".format(self.client.base_url, self.id)
        resp = requests.put(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        return js["activationCode"] 
        
    def delete(self, account_id):
        url = "{0}/accounts/{1}".format(self.client.base_url, account_id)
        resp = requests.delete(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 204)
        
    def getAccountUser(self):
        url = "{0}/accounts/{1}/users".format(self.client.base_url, self.id)
        resp = requests.get(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        return js
        
    def addUser(self, user_info, user_id):
        
        url = "{0}/accounts/{1}/users/{2}".format(self.client.base_url, self.id, user_id)
        data = json.dumps(payload)
        print url, data
        resp = requests.put(url, data=data, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
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
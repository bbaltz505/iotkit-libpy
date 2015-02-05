"""@package Device
Methods for IoT Analytics device management
"""
from globals import *
from utils import *
import requests
import json
import uuid
import os.path

class Device:
    device_id   = None
    client      = None
    account     = None
    device_token = None
    
    def __init__(self, account):
        self.client  = account.client
        self.account = account
        
    def create(self, device_info):
        if device_info:
            url = "{0}/accounts/{1}/devices".format(self.client.base_url, self.account.id)
            data = json.dumps(device_info)
            print url, data
            resp = requests.post(url, data=data, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
            check(resp, 201)
            js = resp.json()
            self.device_id = js["deviceId"]
            return js
        else:
            raise ValueError("No account name given.")
        
    def setDevice(self, device_id, tokenFile):
        if device_id:
            self.device_id = device_id
        else:
            raise ValueError("Device_id not specified.") 
        
        if os.path.isfile(tokenFile):
            js=open(tokenFile)
            data = json.load(js)
            self.device_token = data["device_token"]
            js.close()
        else:
            raise ValueError("Token file not found: ", tokenFile) 
    
    
    def listAll(self):
        url = "{0}/accounts/{1}/devices".format(self.client.base_url, self.account.id)
        resp = requests.get(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        return js 
        
    def getInfo(self, device_id=None):
        if not device_id:
            device_id = self.device_id
        url = "{0}/accounts/{1}/devices/{2}".format(self.client.base_url, self.account.id, device_id)
        resp = requests.get(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        self.device_id = js["deviceId"]
        return js 
        
    def update(self, device_info, device_id=None):
        if not device_id:
            device_id = self.device_id
        url = "{0}/accounts/{1}/devices/{2}".format(self.client.base_url, self.account.id, device_id)
        data = json.dumps(device_info)
        print url, data
        resp = requests.put(url, data=data, headers=get_device_headers(self.device_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        self.device_id = js["deviceId"]
        return js
        
    def activate(self, activation_code):
        url = "{0}/accounts/{1}/devices/{2}/activation".format(self.client.base_url, self.account.id, self.device_id)
        activation = {
            "activationCode": activation_code
        }
        data = json.dumps(activation)
        resp = requests.put(url, data=data, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        self.device_token = js["deviceToken"]
        return self.device_token
        
    def delete(self, device_id):
        url = "{0}/accounts/{1}/devices/{2}".format(self.client.base_url, self.account.id, device_id)        
        resp = requests.delete(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 204)
        
    def addComponent(self, name, type):
        cid = str(uuid.uuid4())
        payload = { 
            "cid": cid,
            "name": name,
            "type": type
        }
        url = "{0}/accounts/{1}/devices/{2}/components".format(self.client.base_url, self.account.id, self.device_id)
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=get_device_headers(self.device_token), proxies=self.client.proxies, verify=g_verify)
        print url, get_device_headers(self.device_token)
        check(resp, 201)
        js = resp.json()
        return js
        
    def deleteComponent(self, cid):        
        url = "{0}/accounts/{1}/devices/{2}/components/{3}".format(self.client.base_url, self.account.id, self.device_id, cid)
        resp = requests.delete(url, headers=get_device_headers(self.device_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 204)
        
    def listTags(self):
        url = "{0}/accounts/{1}/devices/tags".format(self.client.base_url, self.account.id)
        resp = requests.get(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        return js 
        
    def listAttributes(self):
        url = "{0}/accounts/{1}/devices".format(self.client.base_url, self.account.id)
        resp = requests.get(url, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        js = resp.json()
        return js 
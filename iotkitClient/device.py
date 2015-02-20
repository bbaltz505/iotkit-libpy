"""@package Device
Methods for IoT Analytics device management
"""
import globals
from utils import *
import requests
import json
import uuid
import os.path
import time

class Device:
    #device_id   = None
    # client      = None
    # account     = None
    # device_token = None
    #device_name = None
    
    def __init__(self, account, id=None):
        if account:
            self.client  = account.client
            self.account = account
            self.proxies = self.client.proxies
            self.account_id = self.account_id
            if id:
                self.deviceId = id
                try:
                    js = self.getInfo()
                except Exception, e:
                    raise ValueError("Device ID not found: ", id)
            
    def create(self, device_info, activate=False):
        if device_info:
            url = "{0}/accounts/{1}/devices".format(globals.base_url, self.account_id)
            data = json.dumps(device_info)
            resp = requests.post(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.proxies, verify=globals.g_verify)
            check(resp, 201)
            js = resp.json()
            #self.device_id = js["deviceId"]
            self.updateProperties(js)
            if activate:
                activation_code = self.account.renewActivationCode()
                self.activate(activation_code)
            return js
        else:
            raise ValueError("No account name given.")
        
    def loadConfig(self, infile):
        if os.path.isfile(infile):
            js=open(infile)
            data = json.load(js)
            self.updateProperties(data)
            js.close()
            return data
        else:
            raise ValueError("Config file not found: ", tokenFile) 
    
    def saveConfig(self, outfile, overWrite=False):
        if self.deviceId:
            data = self.getInfo()
            data["device_token"] = self.device_token
            #prettyprint(data)
        else:
            raise ValueError("Unknown device - no configuration to save.")
        try:
            if os.path.isfile(outfile) and not overWrite:
                raise RuntimeError("Cannot overwrite existing token file:", outfile)
            else:
                with open(outfile, 'w') as outfile:
                    json.dump(data, outfile)
        except:
            raise RuntimeError("Error writing token:", outfile) 
            
    def listAll(self):
        url = "{0}/accounts/{1}/devices".format(globals.base_url, self.account_id)
        resp = requests.get(url, headers=get_auth_headers(self.client.user_token), proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js 
        
    def getInfo(self, device_id=None):
        if not device_id:
            device_id = self.deviceId
        url = "{0}/accounts/{1}/devices/{2}".format(globals.base_url, self.account_id, device_id)
        resp = requests.get(url, headers=get_auth_headers(self.client.user_token), proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        #self.device_id = js["deviceId"]
        self.updateProperties(js)
        return js 
        
    def searchDevices(self, searchterms):
        if searchterms:
            url = "{0}/accounts/{1}/devices?{2}".format(globals.base_url, self.account_id, searchterms)
            resp = requests.get(url, headers=get_auth_headers(self.client.user_token), proxies=self.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            return js 
        return None
        
    def update(self, device_info, device_id=None):
        if not device_id:
            device_id = self.device_id
        url = "{0}/accounts/{1}/devices/{2}".format(globals.base_url, self.account_id, device_id)
        data = json.dumps(device_info)
        resp = requests.put(url, data=data, headers=get_auth_headers(self.device_token), proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        self.updateProperties(js)
        return js
        
    def activate(self, activation_code):
        url = "{0}/accounts/{1}/devices/{2}/activation".format(globals.base_url, self.account_id, self.deviceId)
        activation = {
            "activationCode": activation_code
        }
        data = json.dumps(activation)
        resp = requests.put(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        self.device_token = js["deviceToken"]
        return self.device_token
        
    def delete(self, device_id=None):
        if not device_id:
            device_id = self.deviceId
        if device_id:
            url = "{0}/accounts/{1}/devices/{2}".format(globals.base_url, self.account_id, device_id)        
            resp = requests.delete(url, headers=get_auth_headers(self.client.user_token), proxies=self.proxies, verify=globals.g_verify)
            check(resp, 204)
            self.deviceId = None
        else:
            raise ValueError("No active device selected.")
            
    # def addComponent(self, name, type):
        # cid = str(uuid.uuid4())
        # payload = { 
            # "cid": cid,
            # "name": name,
            # "type": type
        # }
        # url = "{0}/accounts/{1}/devices/{2}/components".format(globals.base_url, self.account_id, self.device_id)
        # data = json.dumps(payload)
        # resp = requests.post(url, data=data, headers=get_auth_headers(self.device_token), proxies=self.proxies, verify=globals.g_verify)
        # print url, get_auth_headers(self.device_token)
        # check(resp, 201)
        # js = resp.json()
        # return js["cid"]
        
    # def deleteComponent(self, cid):        
        # url = "{0}/accounts/{1}/devices/{2}/components/{3}".format(globals.base_url, self.account_id, self.device_id, cid)
        # resp = requests.delete(url, headers=get_auth_headers(self.device_token), proxies=self.proxies, verify=globals.g_verify)
        # check(resp, 204)
        
    def listTags(self):
        url = "{0}/accounts/{1}/devices/tags".format(globals.base_url, self.account_id)
        resp = requests.get(url, headers=get_auth_headers(self.client.user_token), proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js 
        
    def listAttributes(self):
        url = "{0}/accounts/{1}/devices".format(globals.base_url, self.account_id)
        resp = requests.get(url, headers=get_auth_headers(self.client.user_token), proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js 

    def sendData(self, dataSeries, cid, loc=None):
        url = "{0}/data/{1}".format(globals.base_url, self.deviceId)
            
        series = packageDataSeries(dataSeries, cid, loc)
        payload = {
            "on": time.time(),
            "accountId": self.account_id,
            "data": series  
        }
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=get_auth_headers(self.device_token), proxies=self.proxies, verify=globals.g_verify)
        check(resp, 201)
        return resp.text
        
    def updateProperties(self, var):
        for key, value in var.items():
            setattr(self, key, value) 

# private function
def packageDataSeries(dataSeries, cid, loc):
    packagedSeries = []
    for t, value in dataSeries:
        js = {
                "componentId": cid,
                "on":          t,
                "value":       str(value)
             }
        if loc:
            js["loc"] = loc
            
        packagedSeries.append(js)
    return packagedSeries
       
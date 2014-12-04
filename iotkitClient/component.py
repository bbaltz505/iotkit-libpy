from globals import *
from utils import *
import requests
import json

class Component:
    
    def __init__(self, device):
        self.client  = device.client
        self.account = device.account
        self.device  = device
        self.id      = None
        
    def getComponent(self, component_name, cid=None):
        info = self.device.getInfo()
        #print info
        if 'components' in info:
                components = info["components"]                
                for c in components:
                    #print ">>>>", c
                    if c['name'] == component_name:
                        if cid != None and cid != c['cid']:
                            continue
                        self.id   = c['cid']
                        self.name = c['name']
                        return c
        return None
            
    def addComponent(self, cid, name, type):
        payload = { 
            "cid": cid,
            "name": name,
            "type": type
        }
        url = "{0}/accounts/{1}/devices/{2}/components".format(self.client.base_url, self.account.id, self.device.device_id)
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=get_device_headers(self.device.device_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 201)
        js = resp.json()
        self.id = cid
        self.name = name
        self.type = type
        return js
        
    def deleteComponent(self, cid):        
        url = "{0}/accounts/{1}/devices/{2}/components/{3}".format(self.client.base_url, self.account.id, self.device.device_id, cid)
        resp = requests.delete(url, headers=get_device_headers(self.device.device_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 204)

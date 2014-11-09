from globals import *
from utils import *
import requests

class Data:    
    def __init__(self, account):
        self.client  = account.client
        self.account = account
        
    def get(self, time0, time1, devices, components, output=None):
        url = "{0}/accounts/{1}/data/search".format(self.client.base_url, self.account.id)
        if output:
            url += "?output=" + output
        payload = {
          "from": 0,
          #"to": time1,
          "targetFilter": {
            "deviceList": [
            #  "<ID>"
            ]
          },
          "metrics": [
            # {
              # "id": "<component_id>",
              # "op": "none" // currently it's the only value supported
            # }
          ]
        } 
        for c in components:
            payload["metrics"].append({"id": c, "op": "none"})
        payload["targetFilter"]["deviceList"] = devices
        data = json.dumps(payload)
        print url, data
        resp = requests.post(url, data=data, headers=get_user_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 200)
        if output:
            return resp.text
        else:
            js = resp.json()
            return js
        
    def send(self, device, time, series):
        url = "{0}/data/{1}".format(self.client.base_url, device.device_id)
        payload = {
            "on": time,
            "accountId": self.account.id,
            "data": series  
        }
        data = json.dumps(payload)
        print url, data
        resp = requests.post(url, data=data, headers=get_device_headers(device.device_token), proxies=self.client.proxies, verify=g_verify)
        check(resp, 201)
        return resp.text

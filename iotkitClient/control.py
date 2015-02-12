"""@package User
Methods for IoT Analytics user management
"""
from globals import *
from utils import *
import requests
import json


def sendActuation(self, commands):
    cid = str(uuid.uuid4())
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
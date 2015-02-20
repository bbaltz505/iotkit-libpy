import globals
from utils import *
import requests
import uuid
import json


class Component:

    def __init__(self, device):
        self.client = device.client
        self.account = device.account
        self.device = device
        self.id = None

    def getComponent(self, component_name, cid=None):
        info = self.device.getInfo()
        if 'components' in info:
            components = info["components"]
            for c in components:
                # return first matching component
                if c['name'] == component_name:
                    if cid and cid != c['cid']:
                        continue
                    self.id = c['cid']
                    self.name = c['name']
                    return c
        return None

    def addComponent(self, name, type):
        cid = str(uuid.uuid4())
        payload = {
            "cid": cid,
            "name": name,
            "type": type
        }
        url = "{0}/accounts/{1}/devices/{2}/components".format(
            globals.base_url, self.account.id, self.device.deviceId)
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=get_auth_headers(
            self.device.device_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 201)
        js = resp.json()
        self.id = cid
        self.name = name
        self.type = type
        return js

    def deleteComponent(self, cid):
        url = "{0}/accounts/{1}/devices/{2}/components/{3}".format(
            globals.base_url, self.account.id, self.device.deviceId, cid)
        resp = requests.delete(url, headers=get_auth_headers(
            self.device.device_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 204)

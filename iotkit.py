import socket
import requests
import json
import sys
import time
import uuid

class connect:
    #####################################
    # Set these values first
    #####################################

    proxies = {
        "https": "http://proxy-us.intel.com:911"
    }
    base_url = ''
    g_user_token = ''
    
    user_id = None
    #account_id = None
    verify = True # whether to verify certs
    #####################################

    def get_auth_headers(self):
        headers = {
            'content-type': 'application/json'
        }
        return headers
        
    def get_user_headers(self):
        headers = {
            'Authorization': 'Bearer ' + self.g_user_token,
            'content-type': 'application/json'
        }
        return headers
    
    def check(self, resp, code):
        if resp.status_code != code:
            print "Expected {0}. Got {1} {2}".format(code, resp.status_code, resp.text)
            sys.exit(1)    

    # Given a username and password, get the user token
    def __init__(self, username, password, host):
        api_root = "/v1/api"
        self.base_url = "https://{0}{1}".format(host, api_root)
        url = "{0}/auth/token".format(self.base_url)
        headers = {'content-type': 'application/json'}
        payload = {"username": username, "password": password}
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=headers, proxies=self.proxies, verify=self.verify)
        self.check(resp, 200)
        js = resp.json()
        self.g_user_token = js['token'] 
        
        # get my user_id (uid) within the Intel IoT Analytics Platform
        self.get_user_id()
        print "UserId: {0}".format(self.user_id)

        # for all the accounts I have access to, find the first account 
        # with the name {account_name} and return the account_id (aid)
        #self.account_id = self.get_account_id(account_name)
        #print "AccountId: {0}".format(self.account_id)
        
    # given a user token, get the user_id
    def get_user_id(self):
        url = "{0}/auth/tokenInfo".format(self.base_url)
        resp = requests.get(url, headers=self.get_user_headers(), proxies=self.proxies, verify=self.verify)        
        self.check(resp, 200)
        js = resp.json()
        self.user_id = js["payload"]["sub"]
        
class component:
    def __init__(self, device):        
        self.component_id = ''
        self.component_name = ''
        self.component_type_name = ''
        
        self.iotcomm = device.iotcomm
        self.iotacct = device.iotacct
        self.device  = device

    # Given an account_id and device_id, and a component type name and name - create a component and return the cid
    def create_component(self, component_type_name, component_name):
        url = "{0}/accounts/{1}/devices/{2}/components".format(self.iotcomm.base_url, self.iotacct.account_id, self.device.device_id)
        component = {
            "type": component_type_name,
            "name": component_name,
            "cid": str(uuid.uuid4())
        }
        data = json.dumps(component)
        resp = requests.post(url, data=data, headers=self.device.get_device_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 201)
        self.component_type_name = component_type_name
        self.component_name = component_name
        js = resp.json()
        self.component_id = js["cid"]
        return js["cid"]
        
    def get_component_id(self, component_name):
        url = "{0}/accounts/{1}/devices/{2}".format(self.iotcomm.base_url, self.iotacct.account_id, self.device.device_id)
        resp = requests.get(url, headers=self.iotcomm.get_user_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 200)
        js = resp.json()
        if 'components' in js:
            components = js["components"]
            component_list = []
            for c in components:
                component_list.append(c['name'])
                for k, v in c.iteritems():
                    if 'name' in k and v == component_name:
                        self.component_id = js["cid"]
                        self.component_name = js["name"]
                        self.component_type_name = js["type"]
                        return c['cid']
        print "component name {0} not found.".format(component_name)
        print "Available components are: {0}".format(', '.join(c for c in component_list))
        return None
        
class data:
    def __init__(self, device):
        self.device = device 
        self.iotcomm = device.iotcomm
        self.iotacct = device.iotacct
    
    #get_observations
    def get_data(self, component, search, format):
        outputformat = ''
        if format is 'csv':
            outputformat = "?output=csv"
        #component_id = component.get_component_id(component_name)
        if not component.component_id:
            return
        url = "{0}/accounts/{1}/data/search{2}".format(self.iotcomm.base_url, self.iotacct.account_id, outputformat)        
        data = json.dumps(search)
        resp = requests.post(url, data=data, headers=self.iotcomm.get_user_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 200)
        if outputformat == '':
            js = resp.json()
            if js:
                for point in js['series'][0]['points']:
                    print point['ts'], point['value']
        else:
            js = resp.text
            file = open('data.csv', 'w+')
            file.write(js)
            
    # save data
    def save_data(self, component, now, value):
        url = "{0}/data/{1}".format(self.iotcomm.base_url, self.device.device_id)
        body = {
            "on": now,
            "accountId": self.iotacct.account_id,
            "data": [
                {
                    "componentId": component.component_id,
                    "on": now,
                    "value": str(value),
                }
            ]
        }
        data = json.dumps(body)
        #try:
        resp = requests.post(url, data=data, headers=self.device.get_device_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 201)
        
class device:
    device_token   = ''
    device_id      = ''
    # given a user_id, get the account_id of the associated account with account_name
    # if there are multiple accounts with the same name, return one of them
    def __init__(self, iotcomm, iotacct, device_id, device_info):
        self.iotcomm = iotcomm
        self.iotacct = iotacct
        self.device_id = device_id
        url = "{0}/accounts/{1}/devices".format(iotcomm.base_url, iotacct.account_id)
        resp = requests.get(url, headers=iotcomm.get_user_headers(), proxies=iotcomm.proxies, verify=iotcomm.verify)
        iotcomm.check(resp, 200)
        js = resp.json()
        # existing device
        if self.device_exists(js, device_id):
            # no device_info supplied - just (re)activate
            if device_info is None:
                print "Device exists. Activating...", device_id
                activation_code = self.generate_activation_code()
                self.device_token = self.activate_device(device_id, activation_code)
            else:
                raise NameError("Device already exists.", device_id)
        # new device
        else:
            if device_info is None:
                raise NameError("Device info required to create new device")
            else:
                print "Creating new device...", device_id
                resp = self.create_device(device_id, device_info)
                activation_code = self.generate_activation_code()
                self.device_token = self.activate_device(device_id, activation_code)
    
    def get_device_headers(self):
        headers = {
            'Authorization': 'Bearer ' + self.device_token,
            'content-type': 'application/json'
        }
        return headers
        
    def device_exists(self, list, device_id):
        if list:
            for device in list:
                if device_id in device['deviceId']:
                    return True
        return False
        
    def create_device(self, device_id, device_info):
        url = "{0}/accounts/{1}/devices".format(self.iotcomm.base_url, self.iotacct.account_id)
        data = json.dumps(device_info)
        resp = requests.post(url, data=data, headers=self.iotcomm.get_user_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 201)
        return resp
        
    # This activation code will be good for 60 minutes
    def generate_activation_code(self):
        url = "{0}/accounts/{1}/activationcode/refresh".format(self.iotcomm.base_url, self.iotacct.account_id)
        resp = requests.put(url, headers=self.iotcomm.get_user_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 200)
        js = resp.json()
        activation_code = js["activationCode"]
        return activation_code

    # Activate a device using a valid activation code
    def activate_device(self, device_id, activation_code):
        url = "{0}/accounts/{1}/devices/{2}/activation".format(self.iotcomm.base_url, self.iotacct.account_id, device_id)
        activation = {
            "activationCode": activation_code
        }
        data = json.dumps(activation)
        resp = requests.put(url, data=data, headers=self.iotcomm.get_user_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 200)
        js = resp.json()        
        if "deviceToken" in js:
            token = js["deviceToken"]
            return token
        else:
            print js
            sys.exit(1)
        
class account:
    account_id = ''
    # given a user_id, get the account_id of the associated account with account_name
    # if there are multiple accounts with the same name, return one of them
    def __init__(self, iotcomm, account_name):
        self.iotcomm = iotcomm
        url = "{0}/users/{1}".format(iotcomm.base_url, iotcomm.user_id)
        resp = requests.get(url, headers=iotcomm.get_user_headers(), proxies=iotcomm.proxies, verify=iotcomm.verify)
        iotcomm.check(resp, 200)
        js = resp.json()
        if 'accounts' in js:
            accounts = js["accounts"]
            for k, v in accounts.iteritems():
                if 'name' in v and v["name"] == account_name:
                    self.account_id = k
                    return
        print "Account name {0} not found.".format(account_name)
        print "Available accounts are: {0}".format([v["name"] for k, v in accounts.iteritems()])   
        
    def get_users(self):    
        url = "{0}/accounts/{1}/users".format(self.iotcomm.base_url, self.account_id)
        resp = requests.get(url, headers=self.iotcomm.get_user_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 200)
        js = resp.json()
        return js
        
    def update_user(self, user_id, data):
        url = "{0}/accounts/{1}/users/{2}".format(self.iotcomm.base_url, self.account_id, user_id)
        resp = requests.put(url, data=data, headers=self.iotcomm.get_user_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 200)
        
    def delete_user(self, user_id):
        url = "{0}/users/{1}".format(self.iotcomm.base_url, user_id)
        resp = requests.get(url, headers=self.iotcomm.get_user_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 204)

class user:
    def __init__(self, iotcomm):
        self.iotcomm = iotcomm
        
    def get_user_info(self, user_id):
        url = "{0}/users/{1}".format(self.iotcomm.base_url, user_id)
        resp = requests.get(url, headers=self.iotcomm.get_user_headers(), proxies=self.iotcomm.proxies, verify=self.iotcomm.verify)
        self.iotcomm.check(resp, 200)
        js = resp.json()
        return js
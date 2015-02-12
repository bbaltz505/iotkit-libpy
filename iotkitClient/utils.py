import sys
import json

def check(resp, code):
    if resp.status_code != code:
        raise RuntimeError("Expected {0}. Got {1} {2}".format(code, resp.status_code, resp.text))
        
def get_auth_headers():
    headers = {
        'content-type': 'application/json'
    }
    return headers
    
def get_user_headers(user_token):
    headers = {
        'Authorization': 'Bearer ' + user_token,
        'content-type': 'application/json'
    }
    return headers

def get_device_headers(device_token):
    headers = {
        'Authorization': 'Bearer ' + device_token,
        'content-type': 'application/json'
    }
    return headers 

def prettyprint(js):
    print json.dumps(js, sort_keys=True, indent=4, separators=(',', ': '))
    

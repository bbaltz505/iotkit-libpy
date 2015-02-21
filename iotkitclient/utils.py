import sys
import json
import os


def check(resp, code):
    if resp.status_code != code:
        raise RuntimeError(
            "Expected {0}. Got {1} {2}".format(code, resp.status_code, resp.text))

def get_auth_headers(token=None):
    headers = {
        #'Authorization': 'Bearer ' + token,
        'content-type': 'application/json'
    }
    if token:
        headers["Authorization"] = 'Bearer ' + token
    return headers

def prettyprint(js):
    print json.dumps(js, sort_keys=True, indent=4, separators=(',', ': '))

def update_properties(obj, var):
    if obj and var:
        for key, value in var.items():
            setattr(obj, key, value)
    else:
        raise ValueError("Invalid object %s or dictionary." %
                         (obj.__name__))

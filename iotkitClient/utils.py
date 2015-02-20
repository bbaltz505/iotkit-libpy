import sys
import json
import os


def check(resp, code):
    if resp.status_code != code:
        raise RuntimeError(
            "Expected {0}. Got {1} {2}".format(code, resp.status_code, resp.text))

# def get_auth_headers():
    # headers = {
        # 'content-type': 'application/json'
    # }
    # return headers


def get_auth_headers(token=None):
    headers = {
        #'Authorization': 'Bearer ' + token,
        'content-type': 'application/json'
    }
    if token:
        headers["Authorization"] = 'Bearer ' + token
    return headers

# def get_auth_headers(device_token):
    # headers = {
    # 'Authorization': 'Bearer ' + device_token,
    # 'content-type': 'application/json'
    # }
    # return headers


def prettyprint(js):
    print json.dumps(js, sort_keys=True, indent=4, separators=(',', ': '))

# def loadConfig(infile):
    # if os.path.isfile(infile):
    # obj = sys.modules[__name__]
    # js=open(infile)
    # print js
    # data = json.load(js)
    # updateProperties(obj, data)
    # for key in obj.__dict__:
    # print "%s -> %s" % (key, getattr(obj, key))
    # js.close()
    # return data
    # else:
    # raise ValueError("Config file not found: %s" % infile)


def updateProperties(obj, var):
    if obj and var:
        for key, value in var.items():
            setattr(obj, key, value)
    else:
        raise ValueError("Invalid object %s or dictionary." %
                         (obj.__name__, var.__name__))

from client import Client
from device import Device
from account import Account
from user import User
from data import Data
from component import Component
from utils import prettyprint, update_properties
import json
import os
import sys


# load Configuration file and store values as class attributes
def load_config(infile):
    ''' Load global settings for Cloud connection
      - server name
      - username
      - password
      - proxy server(s)
      - API root location on REST server

    '''
    if os.path.isfile(infile):
        obj = sys.modules[__name__]
        js = open(infile)
        data = json.load(js)
        update_properties(obj, data)
        js.close()
        return data
    else:
        raise ValueError("Config file not found: %s" % infile)

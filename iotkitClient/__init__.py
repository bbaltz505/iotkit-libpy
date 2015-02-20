
from client import Client
from device import Device
from account import Account
from user import User
from data import Data
from component import Component
from utils import prettyprint, updateProperties
import json
import os
import sys


def loadConfig(infile):
    # load Configuration file and store values as class attributes
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
        updateProperties(obj, data)
        js.close()
        return data
    else:
        raise ValueError("Config file not found: %s" % infile)

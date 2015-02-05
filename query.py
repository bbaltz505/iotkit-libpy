#!/usr/bin/python

# Now import your Phone Package.
from iotkitClient.client import Client
from iotkitClient.component import Component
from iotkitClient.device import Device
from iotkitClient.account import Account
from iotkitClient.user import User
from iotkitClient.utils import prettyprint
from iotkitClient.data import Data
import json
import uuid
import time
   
username = "bbaltz@yahoo.com"
password = "Passw0rd"
hostname = "dashboard.us.enableiot.com"
account_name = "iot"
proxies = { "https": "http://proxy-us.intel.com:911" }
device_id = "babaltz-MI"

# make connection to IOTKit dashboard
comm = Client(hostname, username, password, proxies)
acct = Account(comm)
acct.setAccount(account_name)

print "UserId:", comm.user_id
print "Account ID: ", acct.id

dev = Device(comm, acct)
dev.getInfo(device_id)
dev.device_token = acct.load_cert("../iotkit-agent/certs/token.json")

compT = Component(dev)
compP = Component(dev)
compH = Component(dev)

compT.getComponent("temp", "eee0c400-66ac-40e7-a9e8-0dde6ba8f69d")
compP.getComponent("pressure", "521d13e2-f5ff-435d-871c-49f8f352019b")
compH.getComponent("humidity", "3def3248-f4ec-4d4f-94ee-31c14f0ec138")
components = [compT.id, compP.id, compH.id]
time1 = -3600
#time2 = 


data = Data(acct)
js = data.get(time1, None, [device_id], components)
print js






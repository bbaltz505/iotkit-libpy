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
time1 = int(time.time() - 604800) * 1000 # a week ago
time2 = time1 + 60000 # plus 60s

query = {
    #"gatewayIds" : ["<gid1>", "<gid2>"],
    "deviceIds" : ["babaltz-MI"],
    #"componentIds" : ["<cid1>", "<cid2>"],
    "from" :  time1,
    "to" :  time2,
    #"returnedMeasureAttributes" : ["att_1", "att_2"],
    #"showMeasureLocation" :  <true/false>,
    "aggregations":"include",
    #"devCompAttributeFilter" : {
        # "filterName1" : ["filter_value1", "filter_value2"],
        # "filterName2" : ["filter_value1", "filter_value2"]
    # },
    # "measurementAttributeFilter" : {
        # "filterName1" : ["filter_value1", "filter_value2"],
        # "filterName2" : ["filter_value1", "filter_value2"]
    # },
    # "valueFilter" : {
        # "value" : ["filter_value1", "filter_value2"]
    # },
    # "componentRowLimit" :  <limit_value>,
    # "countOnly" :  <true/false>,
    # "sort" : [{
            # "sortField1" : "<sort_order>"
        # }, {
            # "sortField2" : "<sort_order>"
        # }       
    # ]
}

report = {
    "from": time1,
    "to": time2,
    "aggregationMethods": ["average", "min", "max"],
    # "dimensions": ["dim1", "dim2"],
    # "offset": <results_index>, 
    # "limit": <number>, 
    # "countOnly": <true/false>,
    # "outputType": "json",   
    # "deviceIds":["<device1>", "<device2>"],
    # "gatewayIds":["<gateway1>", "<gateway2>"],
    # "componentIds":["<component1>", "<component2>"],
    # "sort": [
        # {"sortField1": "<sortOrder>"},
        # {"sortField2": "<sortOrder>"}
    # ],
    "filters": {
        "componentType": ["temperature.v1.0", "pressure.v1.0"]                
    }
 }


data = Data(acct)
#js = data.advancedQuery(query)
js = data.report(report)
prettyprint(js)






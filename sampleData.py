#!/usr/bin/python
import iotkitClient
import time

# User credentials on IoT Analytics Cloud   
username = "bbaltz@yahoo.com"
password = "Passw0rd"

# REST API server
hostname = "dashboard.us.enableiot.com"

# proxy server info - if needed
proxies = { "https": "http://proxy-us.intel.com:911" }

# Account info 
account_name = "iot"

# Device info
device_id = "babaltz-desk"

# Component info
component_name = "temp"
component_type = "temperature.v1.0"

# Open connection to Cloud to obtain user token
print "Connecting to Cloud:", hostname, username
client = iotkitClient.Client(hostname, username, password, proxies)
print "UserId:", client.user_id

user = iotkitClient.User(client)
iotkitClient.prettyprint(user.setUser())

#account_id = "c349d0ef-a076-413a-a447-aad3038fa185"
#account_id = user.findAccounts(account_name)
account = iotkitClient.Account(client)
account.setAccount(account_name)
print "Account ID: ", account.id

device = iotkitClient.Device(account)
device.setDevice(device_id, "./device.json")
#print device.device_id, device.device_token 

# Create/Register new component
#device.addComponent(component_name, component_type)
component = iotkitClient.Component(device)

component.getComponent(component_name, "19d8fbb2-c2ae-4d06-88bb-7b6df00d8d89")
#component.addComponent(component_name, component_type)

#print "Added component:", component.id, component_name, component_type

data = iotkitClient.Data(account)
time0 = int(time.time())*1000
dataSeries = [ (time0, 34.0),
               (time0+2000, 21.0),
               (time0+4000, 14.0)
             ]
loc = [ 45.5434085, -122.654422, 124.3 ]
sensor_data = data.packageDataSeries(dataSeries, loc, component.id)
#print sensor_data
data.send(device, time.time()*1000, sensor_data)

time0 = (int(time.time())-13600)*1000
time1 = (int(time.time()))*1000
devices = [device_id]
components = [component.id]
#print time0, time1, devices, components
#prettyprint(data.get(time0, time1, devices, components))
advQuery = {
    "deviceIds" : [device_id],
    #"componentIds" : ["<cid1>", "<cid2>"],
    "from" :  time0,
    "to" :  time1,
    #"returnedMeasureAttributes" : ["att_1", "att_2"],
    "showMeasureLocation" :  True,
        #"aggregations":<include/exclude/only>,
    "devCompAttributeFilter" : {
        "component_name" : ["temp"],
        #"filterName2" : ["filter_value1", "filter_value2"]
    },
    # "measurementAttributeFilter" : {
        # "filterName1" : ["filter_value1", "filter_value2"],
        # "filterName2" : ["filter_value1", "filter_value2"]
    # },
    #"valueFilter" : {
    #    "value" : ["filter_value1", "filter_value2"]
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
iotkitClient.prettyprint(advQuery)
iotkitClient.prettyprint(data.advancedQuery(advQuery))

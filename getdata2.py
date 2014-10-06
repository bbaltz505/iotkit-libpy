import iotkit
import sys
import time
import math

# Authentication/Account info
username = "bbaltz@yahoo.com"
password = "Passw0rd"
hostname = "dashboard.us.enableiot.com"
account_name = "Brian Baltz"

# Device/component info
device_id = "foobie3"
device_name = device_id + "-Device"
component_name = "response"

# make connection to IOTKit dashboard
comm = iotkit.connect(username, password, hostname)
acct = iotkit.account(comm, account_name)

device_info = {
        "deviceId": str(device_id),
        "gatewayId": str(device_id),
        "name": device_name,
        "tags": ["US", "California", "San Francisco"],
        # if the device will be static, use this
        # to remember where you put it
        #"loc": [37.783944, -122.401289, 17],
        "attributes": {
            "vendor": "intel",
            "platform": "x86",
            "os": "linux"
        }
    }
    
try:
    device = iotkit.device(comm, acct, device_id, device_info)
except NameError:
    print "Error creating device"
    sys.exit(1)

component = iotkit.component(device)
component.create_component("response.v1.0", component_name)    
data = iotkit.data(device)

print "Submitting data..."
# generate data end submit
t0 = 0
for i in range(1,5):
    x = (time.time() - t0) * 2.0 * 3.14 / 60.0
    value = math.sin(x)
    print x, value
    now = int(time.time() * 1000)
    data.save_data(component, now, value)
    time.sleep(1)
t1 = time.time()     

#retrieve data series
search = {
    "from": 0,
    #"to":   time1,
    "targetFilter": {
        "deviceList": [device.device_id]
    },
    "metrics": [
        {
            "id": component.component_id,
            "op": "none"
        }
    ]#,
    #"queryMeasureLocation": True
}
print "Reading data..."
data.get_data(component, search, None)

 
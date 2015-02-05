#!/usr/bin/python
import iotkitClient

# User credentials on IoT Analytics Cloud   
username = "bbaltz@yahoo.com"
password = "Passw0rd"

# REST API server
hostname = "dashboard.us.enableiot.com"

# proxy server info - if needed
proxies = { "https": "http://proxy-us.intel.com:911" }

# Account info 
account_name = "iot99"

# Device info
device_id = "Junko"
device_name = "Device-Junko"

# Component info
component_name = "temp"
component_type = "temperature.v1.0"

# Open connection to Cloud to obtain user token
print "Connecting to Cloud:", hostname, username
client = iotkitClient.Client(hostname, username, password, proxies)
print "UserId:", client.user_id

# Create new account
print "Creating account:", account_name
account = iotkitClient.Account(client)
account.create(account_name)

# Obtain new user token with access to new account
client.reinit(username, password)
print "Account ID:", account.id
iotkitClient.prettyprint(account.getInfo())

# Create new device
device = iotkitClient.Device(account)
device_info = { 
    "deviceId": device_id,
    "gatewayId": device_id,
    "name": "Device #1",            
    "tags": ["US", "California", "Sacramento"],
    "loc": [ 45.5434085, -122.654422, 124.3 ],
    "attributes": {
        "vendor": "intel",
        "platform": "x86",
        "os": "linux"
    }
}

# Delete device if it already exists
try:
    device.delete(device_id)
except:
    print "Error during delete!!"

print "Creating device:", device_id
js = device.create(device_info)

# Obtain activation code and activate device
activation_code = account.renewActivationCode()
print "Activating device. Code =", activation_code
device_token = device.activate(activation_code)
print "Device activated. Token=", device_token

# Create/Register new component
#cid = str(uuid.uuid4())
print "Adding component", component_name, component_type
js = device.addComponent(component_name, component_type)
cid = js["cid"]

# Update device-info
device_info = { 
    "gatewayId": device_id,
    "name": "Device #1",            
    "tags": ["USSR", "Ukraine", "Kiev"],
    "loc": [ 45.5434085, -122.654422, 124.3 ],
    "attributes": {
        "vendor": "intel",
        "platform": "x86",
        "os": "linux"
    }
}

print "Updating device_info", device_info
device.update(device_info)
print "Getting device_info"
iotkitClient.prettyprint(device.getInfo())

# Cleanup
# Delete component
print "Deleting component", component_name
device.deleteComponent(cid)

# Delete device
print "Deleting device", device_id
device.delete(device_id)

# Delete account
print "Deleting account:", account_name, account.id
account.delete(account.id)










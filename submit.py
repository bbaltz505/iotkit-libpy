import iotkitClient
import time

# js = iotkitClient.__dict__
# for key, value in iotkitClient.__dict__.items():
    # print "%s = %s" % (str(key), str(getattr(iotkitClient, key))) 
iotkitClient.loadConfig("config.json")
print iotkitClient.proxies

proxies = { "https": "http://proxy-us.intel.com:911" }

device = iotkitClient.Device(None)
device.loadConfig("device.json")
device.proxies = proxies
print device.device_token
print device.sensors
# for key, value in iotkitClient.__dict__.items():
    # print "%s = %s" % (str(key), str(getattr(iotkitClient, key))) 
#device.deviceId = device.device_id
comp = (item for item in device.sensors if item["name"] == "temp").next()
cid = comp["cid"]
now = int(time.time()*1000)
data = [(now, 34.0)]
print data

device.sendData(data, cid)
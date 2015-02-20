import iotkitClient
import unittest
from config import *

# Test vars
deviceid = "Junko"
info = { 
            "deviceId": deviceid,
            "gatewayId": deviceid,
            "name": "Device #1",            
            "tags": ["US", "California", "Sacramento"],
            "loc": [ 45.5434085, -122.654422, 124.3 ],
            "attributes": {
                "vendor": "intel",
                "platform": "x86",
                "os": "linux"
            }
        }
componentName = "temp"
componentType = "temperature.v1.0"

class TestDeviceMgmnt(unittest.TestCase):
        
    # login once, for all tests. Delete all test accounts
    @classmethod
    def setUpClass(cls):
        global iot, acct
        iot = iotkitClient.Client(username, password, proxies)
        acct = iotkitClient.Account(iot)
        acct.getAccount(account_name)
        
    def create(self, activate=False):
        device = iotkitClient.Device(acct)
        js = device.create(info, activate)
        # if activate:
            # code = acct.renewActivationCode()
            # device.activate(code)
        return device
        
    # def delete(self):
        # device = iotkitClient.Device(acct)
        # js = device.delete()
        
    def setUp(self):
        # try:
        device = iotkitClient.Device(acct, deviceid)
        device.delete()
        # except: 
            # pass        

    def bulkcreate(self):
        for i in (range(4)):
            device = iotkitClient.Device(acct)
            info["deviceId"] = deviceid + str(i)
            js = device.create(info)

    def bulkdelete(self):
        for i in (range(4)):
            device = iotkitClient.Device(acct)
            name = deviceid + str(i)
            js = device.delete()
        
    # Connection tests
    def test_create_device(self):
        device = iotkitClient.Device(acct)
        info = { 
                    "deviceId": deviceid,
                    "gatewayId": deviceid,
                    "name": "Device #1",            
                    "tags": ["US", "California", "Sacramento"],
                    "loc": [ 45.5434085, -122.654422, 124.3 ],
                    "attributes": {
                        "vendor": "intel",
                        "platform": "x86",
                        "os": "linux"
                    }
                }
        js = device.create(info)
        self.assertEqual(js["deviceId"], deviceid)
        self.assertEqual(js["status"], "created")
    
    def test_listAll_devices(self):
        device = self.create()
        devlist = device.listAll()
        self.assertTrue(devlist)
    
    def test_delete_device(self):
        device = self.create()
        device.delete()
        
    # def test_list_filtered_devices(self):
        # try:
            # self.bulkdelete()    # delete - just in case
        # except:
            # pass
        # self.bulkcreate()
        # code = acct.renewActivationCode()
        # self.assertTrue(code)
        # device = iotkitClient.Device(acct, deviceid + "1")
        # device.activate(code)  # activate Junko1
        # device = iotkitClient.Device(acct, deviceid + "2")
        # device.activate(code)  # activate Junko2
        # search = "status=created&sort=name&order=desc"
        # js = device.searchDevices(search)
        # iotkitClient.prettyprint(js)
        # self.assertTrue(len(js), 2) # check for 2 returned devices
        # self.assertEqual(js[0]["deviceId"], "Junko2")
        # self.assertEqual(js[1]["deviceId"], "Junko1") # check for descending order
        # self.bulkdelete()
        
    def test_addComponent(self):
        device = self.create(activate=True)
        comp = iotkitClient.Component(device)
        comp.addComponent(componentName, componentType)
        self.assertTrue(comp.id)
        
    def test_deleteComponent(self):
        device = self.create(activate=True)
        comp = iotkitClient.Component(device)
        comp.addComponent(componentName, componentType)
        self.assertTrue(comp.id)
        comp.deleteComponent(comp.id)
        
    def test_config(self):
        device = self.create(activate=True)
        comp = iotkitClient.Component(device)
        comp.addComponent(componentName, componentType)
        device.saveConfig("foo.json", True)
        info = device.loadConfig("foo.json")
        iotkitClient.prettyprint(info)
        for key, value in info.items():
            print "%s = %s = %s" % (key, str(value), str(getattr(device, key)))
            self.assertEqual(value, getattr(device, key))
        pass
        
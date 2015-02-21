import iotkitclient
import unittest
from config import *

# Test vars
deviceid = "Junko"
info = {
    "deviceId": deviceid,
    "gatewayId": deviceid,
    "name": "Device #1",
            "tags": ["US", "California", "Sacramento"],
            "loc": [45.5434085, -122.654422, 124.3],
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
        iot = iotkitclient.Client(username, password, proxies)
        acct = iotkitclient.Account(iot)
        acct.get_account(account_name)
        while True:
            try:
                device = iotkitclient.Device(acct, deviceid)
                print "Deleting ", deviceid
                device.delete()
            except:
                break

    def create(self, activate=False):
        device = iotkitclient.Device(acct)
        js = device.create(info, activate)
        # if activate:
        # code = acct.renew_activation_code()
        # device.activate(code)
        return device

    def delete(self, name):
        device = iotkitclient.Device(acct, name)
        js = device.delete()

    def setUp(self):
        try:
            self.delete(deviceid)
        except:
            pass

    def bulkcreate(self):
        for i in (range(4)):
            device = iotkitclient.Device(acct)
            info["deviceId"] = deviceid + str(i)
            js = device.create(info)

    def bulkdelete(self):
        for i in (range(4)):
            device = iotkitclient.Device(acct)
            name = deviceid + str(i)
            js = device.delete()

    # Connection tests
    def test_create_device(self):
        device = iotkitclient.Device(acct)
        info = {
            "deviceId": deviceid,
            "gatewayId": deviceid,
            "name": "Device #1",
                    "tags": ["US", "California", "Sacramento"],
                    "loc": [45.5434085, -122.654422, 124.3],
                    "attributes": {
                        "vendor": "intel",
                        "platform": "x86",
                        "os": "linux"
                    }
        }
        js = device.create(info)
        self.assertEqual(js["deviceId"], deviceid)
        self.assertEqual(js["status"], "created")

    def test_list_all_devices(self):
        device = self.create()
        devlist = device.list_all()
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
        # code = acct.renew_activation_code()
        # self.assertTrue(code)
        # device = iotkitclient.Device(acct, deviceid + "1")
        # device.activate(code)  # activate Junko1
        # device = iotkitclient.Device(acct, deviceid + "2")
        # device.activate(code)  # activate Junko2
        # search = "status=created&sort=name&order=desc"
        # js = device.searchDevices(search)
        # iotkitclient.prettyprint(js)
        # self.assertTrue(len(js), 2) # check for 2 returned devices
        # self.assertEqual(js[0]["deviceId"], "Junko2")
        # self.assertEqual(js[1]["deviceId"], "Junko1") # check for descending order
        # self.bulkdelete()

    def test_add_component(self):
        device = self.create(activate=True)
        comp = iotkitclient.Component(device)
        comp.add_component(componentName, componentType)
        self.assertTrue(comp.id)

    def test_deleteComponent(self):
        device = self.create(activate=True)
        comp = iotkitclient.Component(device)
        comp.add_component(componentName, componentType)
        self.assertTrue(comp.id)
        comp.delete_component(comp.id)

    def test_config(self):
        device = self.create(activate=True)
        comp = iotkitclient.Component(device)
        comp.add_component(componentName, componentType)
        device.save_config("foo.json", True)
        info = device.load_config("foo.json")
        #iotkitclient.prettyprint(info)
        for key, value in info.items():
            #print "%s = %s = %s" % (key, str(value), str(getattr(device, key)))
            self.assertEqual(value, getattr(device, key))
        pass

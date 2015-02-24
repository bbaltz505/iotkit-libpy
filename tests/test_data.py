import iotkitclient
import unittest
from config import *
import uuid
import time

# Test vars
deviceid = "Junko"
configFile = "device.json"
componentName = "temp"
componentType = "temperature.v1.0"
loc = [45.5434085, -122.654422, 124.3]
device_info = {
    "deviceId": deviceid,
    "gatewayId": deviceid,
    "name": deviceid + "-device",
    "tags": ["US", "California", "Sacramento"],
    "loc": loc,
    "attributes": {
        "vendor": "intel",
        "platform": "x86",
        "os": "linux"
    }
}
data = None


class TestDataMgmnt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global iot, acct, device, comp, data, t0, t1
        iot = iotkitclient.Client(host=hostname, proxies=proxies)
        iot.login(username, password)
        acct = iotkitclient.Account(iot)
        try:
            acct.get_account(account_name)
        except:
            acct.create(account_name)
            iot.reinit(username, password)
            
        device = iotkitclient.Device(acct)
        try:
            device.delete(deviceid)
        except:
            pass
        device.create(device_info, activate=True)
        device.save_config(configFile, True)
        comp = iotkitclient.Component(device)
        comp.add_component(componentName, componentType)
        # submit sample data
        t0 = int(time.time() * 1000)  # current time in msec
        t1 = int((time.time() + 1) * 1000)  # current time in msec
        data = [(t0, 45.0), (t1, 55.0)]
        
        device.send_data(device.package_data_series(data, comp.id, loc))
        time.sleep(5)

    def create(self, activate=False):
        device = iotkitclient.Device(acct)
        js = device.create(device_info, activate=True)
        return device

    # def setUp(self):

    def test_query1(self):
        results = acct.get_data(t0, t1, [device.deviceId], [comp.id])
        self.assertTrue(results)
        print results
        # results[0] - data for device='Junko'; points[0] - 1st returned data
        # set
        self.assertEqual(float(results[0]["points"][0]["value"]), data[0][1])
        self.assertEqual(float(results[0]["points"][1]["value"]), data[1][1])

    def test_query2(self):
        results = acct.get_data(t0, t1, [device.deviceId], [comp.id], csv=True)
        expected = "Device Id,Device Name,Component Id,Component Name,Component Type,Time Stamp,Value\n"
        expected += "%s,%s,%s,%s,%s,%s,%s\n" % (device.deviceId, device.name, comp.id, componentName, componentType,
                                                data[0][0], data[0][1])
        expected += "%s,%s,%s,%s,%s,%s,%s" % (device.deviceId, device.name, comp.id, componentName, componentType,
                                              data[1][0], data[1][1])
        self.assertEqual(results, expected)

    def test_advquery1(self):
        query = {
            "deviceIds": [device.deviceId],
            "from": t0,
            "to": t1,
        }
        results = acct.advanced_query(query)
        self.assertEqual(results["accountId"], acct.id)
        self.assertEqual(
            float(results["data"][0]["components"][0]["samples"][0][1]), data[0][1])
        self.assertEqual(
            float(results["data"][0]["components"][0]["samples"][1][1]), data[1][1])

    def test_report(self):
        now = int(time.time() * 1000)  # current time in msec
        report = {
            "from": t0,
            "to": t1,
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
        print t0, t1, data
        iotkitclient.prettyprint(report)
        js = acct.data_report(report)
        # print js
        iotkitclient.prettyprint(js)
        self.assertTrue(js)

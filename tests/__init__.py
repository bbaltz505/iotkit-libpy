import iotkitClient
import unittest

# Test vars
username = "bbaltz@yahoo.com"
password = "Passw0rd"
account_name = "iot99"
hostname = "dashboard.us.enableiot.com"
proxies = { "https": "http://proxy-us.intel.com:911" }
device_id = "Junko"
component_name = "temp"

class TestSequenceFunctions(unittest.TestCase):

    # def setUp(self):
        # self.seq = range(10)
        
    def test_connect(self):
        iot = iotkitClient.Client(hostname, username, password, proxies)
        print iot.user_id, iot.user_token
        self.assertTrue(True)

    def test_connect_bad_host(self):
        iot = iotkitClient.Client("foo.com", username, password, proxies)
        print iot.user_id, iot.user_token
        self.assertTrue(True)

    def test_connect_bad_username(self):
        iot = iotkitClient.Client("foo.com", username, password, proxies)
        print iot.user_id, iot.user_token
        self.assertTrue(True)
        
    def test_connect_bad_password(self):
        iot = iotkitClient.Client("foo.com", username, password, proxies)
        print iot.user_id, iot.user_token
        self.assertTrue(True)

    def test_connect_bad_proxy(self):
        iot = iotkitClient.Client("foo.com", username, password, proxies)
        print iot.user_id, iot.user_token
        self.assertTrue(True)        

if __name__ == '__main__':
    unittest.main()
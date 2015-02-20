import iotkitClient
import unittest
from config import *

# Test vars
badproxies = { "https": "http://xxx.intel.com:911" }
iot_version = "0.12.0"

class TestAuthentication(unittest.TestCase):
        
    def login(self):
        return iotkitClient.Client(hostname, username, password, proxies)
    
    # Connection tests
    def test_connect(self):
        iot = self.login()
        self.assertTrue(iot.user_token)

    def test_connect_bad_host1(self):
        self.assertRaises(RuntimeError, iotkitClient.Client,
                                        "foo.com", username, password, proxies) 
        
    def test_connect_bad_host2(self):
        self.assertRaises(ValueError, iotkitClient.Client,
                                      None, username, password, proxies)

    def test_connect_bad_username1(self):
        self.assertRaises(RuntimeError, iotkitClient.Client,
                                      hostname, "foo@boo.com", password, proxies) 

    def test_connect_bad_username2(self):
        self.assertRaises(ValueError, iotkitClient.Client,
                                      hostname, None, password, proxies) 
                                      
    def test_connect_bad_password1(self):
        self.assertRaises(ValueError, iotkitClient.Client,
                                      hostname, username, None, proxies)
    def test_connect_bad_password2(self):
        self.assertRaises(RuntimeError, iotkitClient.Client,
                                      hostname, username, "xxx", proxies)
                                      
    def test_connect_bad_proxy(self):
        self.assertRaises(RuntimeError, iotkitClient.Client,
                                      hostname, username, password, badproxies)       
                                      
    # # GetUserTokenInfo tests
    def test_get_user_tokeninfo1(self):
        iot = self.login()
        utoken = iot.get_user_tokeninfo()    
        self.assertTrue(utoken["payload"])
        
    # Health API
    def test_getVersion1(self):
        iot = self.login()
        version = iot.getVersion()
        self.assertEqual(iot_version, version["build"])

    def test_getVersion2(self):
        version = iotkitClient.Client.getVersion(proxies)
        self.assertEqual(iot_version, version["build"])
        
    # Re-initialize to get new token (use after creating a new account)
    def test_reinit(self):
        iot = self.login()
        utoken = iot.user_token  # initial token
        iot.reinit(username, password)  # get new new token
        self.assertNotEqual(iot.user_token, utoken)
        
    def test_bad_reinit_bad_user1(self):
        iot = self.login()    
        self.assertRaises(ValueError, iot.reinit, None, password)
        
    def test_bad_reinit_bad_user2(self):
        iot = self.login()    
        self.assertRaises(ValueError, iot.reinit, "", password)
        
    def test_bad_reinit_bad_password1(self):        
        iot = self.login() 
        self.assertRaises(ValueError, iot.reinit, username, None)
        
    def test_bad_reinit_bad_password2(self):        
        iot = self.login() 
        self.assertRaises(RuntimeError, iot.reinit, username, "xxxxx")
        
# if __name__ == '__main__':
    # unittest.main()
suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthentication)
#unittest.TextTestRunner(verbosity=2).run(suite)
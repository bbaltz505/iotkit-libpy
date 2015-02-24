import iotkitclient
import unittest
from config import *

# Test vars
badproxies = {"https": "http://xxx.intel.com:911"}
iot_version = "0.12.2"


class TestAuthentication(unittest.TestCase):

    def login(self):
        iot = iotkitclient.Client(host=hostname, proxies=proxies)
        iot.login(username, password)
        return iot

    # Connection tests
    def test_connect(self):
        iot = self.login()
        self.assertTrue(iot.user_token)

    def test_connect_bad_host1(self):
        self.assertRaises(RuntimeError, iotkitclient.Client,
                          "enableiot2.com", proxies)
                          
    def test_connect_default_host(self):
        iot = iotkitclient.Client(None, proxies)
                          
    def test_connect_bad_username1(self):
        iot = iotkitclient.Client(host=hostname, proxies=proxies)
        self.assertRaises(RuntimeError, iot.login,
                          "foo@boo.com", password)

    def test_connect_bad_username2(self):
        iot = iotkitclient.Client(host=hostname, proxies=proxies)
        self.assertRaises(ValueError, iot.login,
                          None, password)

    def test_connect_bad_password1(self):
        iot = iotkitclient.Client(host=hostname, proxies=proxies)
        self.assertRaises(ValueError, iot.login,
                          username, None)

    def test_connect_bad_password2(self):
        iot = iotkitclient.Client(host=hostname, proxies=proxies)
        self.assertRaises(RuntimeError, iot.login,
                          username, "xxx")

    def test_connect_bad_proxy(self):
        self.assertRaises(RuntimeError, iotkitclient.Client,
                          hostname, badproxies)

    # GetUserTokenInfo tests
    def test_get_user_tokeninfo1(self):
        iot = self.login()
        utoken = iot.get_user_tokeninfo()
        self.assertTrue(utoken["payload"])
        
    # Health API
    def test_getVersion(self):
        iot = self.login()
        version = iot.get_version()
        self.assertEqual(iot_version, version["build"])
        
    # Health API - unauthenticated
    def test_getVersion(self):
        iot = iotkitclient.Client(hostname, proxies)
        version = iot.get_version()
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


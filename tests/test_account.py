import iotkitclient
import unittest
from config import *

# Test vars
badproxies = {"https": "http://xxx.intel.com:911"}
iot_version = "0.12.0"
newaccount = "Test101"


class TestAccountMgmt(unittest.TestCase):
    # utility functions
    # create an account

    def create(self, name):
        # acct = iotkitclient.Account(iot)
        # acct.create(name)
        # return acct
        return self.get(name)

    # get account info
    def get(self, name):
        acct = iotkitclient.Account(iot)
        id = acct.get_account(name)
        return acct

    # delete an account
    @classmethod
    def delete(cls, name):
        global acct
        acct.get_account(name)
        if acct.id:
            print "Found ", newaccount, acct.id, "deleting..."
            acct.delete(acct.id)

    # delete all test accounts
    @classmethod
    def deleteAll(cls, name):
        while True:
            try:
                cls.delete(name)
            except:
                break

    # login once, for all tests. Delete all test accounts
    # create one test account to use to avoid throttling
    @classmethod
    def setUpClass(cls):
        global iot, acct
        iot = iotkitclient.Client(host=hostname, proxies=proxies)
        iot.login(username, password)
        acct = iotkitclient.Account(iot)
        cls.deleteAll(newaccount)
        acct.create(newaccount)
        iot.reinit(username, password)

    ########################################
    # Connection tests
    def test_get(self):
        acct2 = iotkitclient.Account(iot)
        acct2.get_account(newaccount)
        self.assertEqual(acct.id, acct2.id)

    # Connection tests
    def test_get_info(self):
        iot.reinit(username, password)
        info = acct.get_info()
        self.assertEqual(newaccount, info["name"])

    # Connection tests
    def test_update(self):
        iot.reinit(username, password)
        cd_execution_frequency = 999
        newinfo = {
            "name": newaccount,
            "cd_execution_frequency": cd_execution_frequency
        }
        acct.update(newinfo)
        info = acct.get_info()
        self.assertEqual(
            cd_execution_frequency, info["cd_execution_frequency"])

    def test_activation_code(self):
        code = acct.get_activation_code()
        self.assertTrue(code)

    def test_renew_activation_code(self):
        code1 = acct.get_activation_code()
        code2 = acct.renew_activation_code()
        self.assertTrue(code2)
        self.assertNotEqual(code1, code2)

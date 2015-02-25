import iotkitclient
import unittest
from config import *

# Test vars
newaccount = "Test101"


class TestAlerts(unittest.TestCase):

    def login(self):
        iot = iotkitclient.Client(host=hostname, proxies=proxies)
        iot.login(username, password)
        return iot

    # Connection tests
    def test_list_alerts(self):
        iot = self.login()
        acct = iotkitclient.Account(iot)
        acct.get_account(newaccount)
        js = acct.list_alerts()
        iotkitclient.prettyprint(js)
        self.assertEqual(0, len(js))
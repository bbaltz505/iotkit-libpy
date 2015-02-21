import iotkitclient
import unittest
import uuid
from config import *

# Test vars
newusername = "foo2@yopmail.com"
newpassword = "junkyW00"

class TestUserMgmt(unittest.TestCase):
    # login once, for all tests. Delete all test accounts

    @classmethod
    def setUpClass(cls):
        global iot
        iot = iotkitclient.Client(username, password, proxies)

    # tests 
    #####################
    
    # run this test first, separately
    # def test_add_user(self):
        # user = iotkitclient.User(iot)
        # user.add_user(newusername, newpassword)
        # self.assertTrue(user.id)

    def test_update_user1(self):
        iot2 = iotkitclient.Client(newusername, newpassword, proxies)
        user = iotkitclient.User(iot2)
        myid = str(uuid.uuid4())  # unique UUID
        info = {
            "attributes": {
                "myid": myid
            }
        }
        js = user.update_user(info)

    def test_update_user2(self):
        iot2 = iotkitclient.Client(newusername, newpassword, proxies)
        user = iotkitclient.User(iot2)
        info = ""  # empty info
        self.assertRaises(ValueError, user.update_user, info)

    def test_get_userinfo(self):
        iot2 = iotkitclient.Client(newusername, newpassword, proxies)
        user = iotkitclient.User(iot2)
        myid = str(uuid.uuid4())  # unique UUID
        info = {
            "attributes": {
                "myid": myid
            }
        }
        js = user.update_user(info)
        js = user.get_info()
        self.assertEqual(js["attributes"]["myid"], myid)

    # def test_delete_user(self):
        # iot2 = iotkitclient.Client(newusername, newpassword, proxies)
        # user2 = iotkitclient.User(iot2)
        # user2.delete_user(user2.id)

    def test_change_user_password(self):
        newpassword2 = "WikiWikiW00"
        # change password
        user = iotkitclient.User(iot)
        user.change_password(newusername, newpassword, newpassword2)
        # check user can login w/ new password
        iot2 = iotkitclient.Client(newusername, newpassword2, proxies) 
        # change password back        
        user = iotkitclient.User(iot2)
        user.change_password(newusername, newpassword2, newpassword)

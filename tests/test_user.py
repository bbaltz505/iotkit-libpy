import iotkitClient
import unittest
from config import *
import uuid

# Test vars
newusername = "foo2@yopmail.com"
newpassword = "junkyW00"

class TestUserMgmt(unittest.TestCase):    
    # login once, for all tests. Delete all test accounts
    @classmethod
    def setUpClass(cls):
        global iot
        iot = iotkitClient.Client(username, password, proxies)
        
    # def test_add_user(self):
        # user = iotkitClient.User(iot)
        # user.addUser(newusername, newpassword)
        # self.assertTrue(user.id)

    # def test_update_user1(self):    
        # iot2 = iotkitClient.Client(hostname, newusername, newpassword, proxies)
        # user = iotkitClient.User(iot2)
        # myid = str(uuid.uuid4())  # unique UUID
        # info = {
                # "attributes":{
                    # "myid":myid
                    # }
               # }
        # js = user.updateUser(info)
        
    # def test_update_user2(self):    
        # iot2 = iotkitClient.Client(hostname, newusername, newpassword, proxies)
        # user = iotkitClient.User(iot2)
        # info = ""  # empty info
        # self.assertRaises(ValueError, user.updateUser, info)
        
    # def test_get_userinfo(self):    
        # iot2 = iotkitClient.Client(hostname, newusername, newpassword, proxies)
        # user = iotkitClient.User(iot2)
        # myid = str(uuid.uuid4())  # unique UUID
        # info = {
                # "attributes":{
                    # "myid":myid
                    # }
               # }
        # js = user.updateUser(info)
        # js = user.getInfo()
        # self.assertEqual(js["attributes"]["myid"], myid)
    
    # def test_delete_user(self):
        # iot2 = iotkitClient.Client(hostname, newusername, newpassword, proxies)
        # user2 = iotkitClient.User(iot2)
        # user2.deleteUser(user2.id)
        
    def test_change_user_password(self):
        user = iotkitClient.User(iot)
        newpassword2 = "WikiWikiW00"
        # change password
        user.changePassword(newusername, newpassword, newpassword2)
        # check user can login w/ new password
        iot2 = iotkitClient.Client(newusername, newpassword2, proxies)
        # change password back
        user.changePassword(newusername, newpassword2, newpassword)

        
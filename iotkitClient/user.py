"""@package User
Methods for IoT Analytics user management
"""
import globals
from utils import *
import requests
import json


class User:
    id = None
    client = None

    def __init__(self, client):
        self.client = client
        js = client.get_user_tokeninfo()
        if js["payload"]["sub"]:
            self.id = js["payload"]["sub"]

    def addUser(self, email, password, toc=True):
        if email and password:
            # given a user_id, get the user's info
            # if toc:
                # toc = "true"
            # else:
                # toc = "false"
            payload = {
                "email": email,
                "password": password,
                "termsAndConditions": toc
            }
            url = "{0}/users".format(globals.base_url)
            data = json.dumps(payload)
            # prettyprint(data)
            resp = requests.post(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 201)
            js = resp.json()
            self.id = js["id"]
            return js
        else:
            raise ValueError("Invalid username or password.")
        return None

    def getInfo(self):
        # Get the user's info
        url = "{0}/users/{1}".format(globals.base_url, self.id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    def deleteUser(self, user_id):
        # Get the user's info
        url = "{0}/users/{1}".format(globals.base_url, user_id)
        resp = requests.delete(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 204)

    def updateUser(self, user_info):
        if user_info:
            # given a user_id, get the user's info
            url = "{0}/users/{1}".format(globals.base_url, self.id)
            data = json.dumps(user_info)
            resp = requests.put(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
        else:
            raise ValueError("No user info given.")
        return None

    def changePassword(self, username, oldpassword, newpassword):
        if username and oldpassword and newpassword:
            # given a user_id, get the user's info
            url = "{0}/users/{1}/change_password".format(
                globals.base_url, username)
            payload = {
                "currentpwd": oldpassword,
                "password": newpassword
            }
            data = json.dumps(payload)
            resp = requests.put(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
        else:
            raise ValueError("No username, old or new password given.")
        return None

    def findAccounts(self, account_name, firstAccountOnly=True):
        accounts = []
        if account_name:
            js = self.setUser()
            if js["accounts"]:
                for account, value in js["accounts"].items():
                    if value["name"] == account_name:
                        accounts.append(account)
        else:
            raise ValueError("No account_name given.")

        if firstAccountOnly:
            return accounts[0]
        return accounts

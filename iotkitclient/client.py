"""@package Client
Methods for IoT Analytics Cloud connections

"""
from utils import *
import globals
import json
import requests


class Client:

    """ IoT Analytics Cloud connection class

    Attributes:
      proxies (str): proxy server used for connection
      user_token (str): access token from IoT Analytics site connection
      user_id (str): user ID for authenticated user
    """
    proxies = ''
    #base_url    = ''
    user_token = ''
    user_id = ''

    def __init__(self, username, password, proxies=None):
        """ Creates IoT Analytics user session

        Args:
        ----------
        username (str): username for IoT Analytics site
        password (str): password for IoT Analytics site
        proxies (str, optional): list of proxy server addresses
          (e.g., {"https": "http://proxy-us.mycorp.com:8080"}

        """
        if not username or not password:
            raise ValueError(
                "Invalid parameter: Client(username, password, [proxies])")
        try:
            self.proxies = proxies
            url = "{0}/auth/token".format(globals.base_url)
            headers = {'content-type': 'application/json'}
            payload = {"username": username, "password": password}
            data = json.dumps(payload)
            resp = requests.post(
                url, data=data, headers=headers, proxies=self.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            self.user_token = js['token']

            # get my user_id (uid) within the Intel IoT Analytics Platform
            js = self.get_user_tokeninfo()
            self.user_id = js["payload"]["sub"]

        except Exception, err:
            raise RuntimeError('Auth ERROR: %s\n' % str(err))

    # given a user token, get the user_id
    def get_user_tokeninfo(self):
        """ Get user token details

        Returns:
        --------
        JSON message containing access token details
        e.g.,
        Response 200 OK (application/json)
            {
                "header": {
                    "typ": "JWT",
                    "alg": "RS256"
                },
                "payload": {
                    "jti": "7b1430a2-dd61-4a47-919c-495cadb1ea7b",
                    "iss": "http://enableiot.com",
                    "sub": "53fdff4418b547e4241b8358",
                    "exp": "2014-10-02T07:53:25.361Z"
                }
            }

        """
        url = "{0}/auth/tokenInfo".format(globals.base_url)
        headers = {'content-type': 'application/json'}
        resp = requests.get(url, headers=get_auth_headers(
            self.user_token), proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    # Health API
    def get_version(self):
        """ Get Cloud version and health information

        Returns:
        --------
        {
            "kind": "healthcheck",
            "isHealthy": true,
            "currentSetting": "prod",
            "name": "iotkit-dashboard",
            "build": "0.12.2",
            "date": "2015-02-19T15:11:05.907Z",
            "items": []
        }

        """
        url = "{0}/health".format(globals.base_url)
        headers = {'content-type': 'application/json'}
        resp = requests.get(
            url, headers=headers, proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    # Re-initialize to get new token (use after creating a new account)
    def reinit(self, username, password):
        """ Re-authenticate to obtain new access token

        Args:
        -----
          username (str): username for IoT Analytics site
          password (str): password for IoT Analytics site

        Returns:
          user_token (str): updated access token

        """
        if not username or not password:
            raise ValueError("Invalid parameter: reinit(username, password)")
        url = "{0}/auth/token".format(globals.base_url)
        headers = {'content-type': 'application/json'}
        payload = {"username": username, "password": password}
        data = json.dumps(payload)
        resp = requests.post(
            url, data=data, headers=headers, proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        self.user_token = js['token']

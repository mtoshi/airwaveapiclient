# -*- coding: utf-8 -*-

"""UnitTests for airwaveapiclient."""

import unittest
import requests
from httmock import all_requests, response, HTTMock
from airwaveapiclient import AirWaveAPIClient


# pylint: disable=unused-argument
@all_requests
def content_login(url, request):
    """Test content for login."""
    cookie_key = 'Mercury::Handler::AuthCookieHandler_AMPAuth'
    cookie_val = '01234567890abcdef01234567890abcd'
    headers = {'Set-Cookie': '%s=%s;' % (cookie_key, cookie_val)}
    content = '<html>html content.</html>'
    return response(200, content, headers, None, 5, request)


class UnitTests(unittest.TestCase):

    """Class UnitTests.

    Unit test for airwaveapiclient.

    """

    def setUp(self):
        """Setup."""
        self.username = 'username'
        self.password = 'password'
        self.address = '192.168.1.1'

    def test_init(self):
        """Test init."""
        obj = AirWaveAPIClient(username=self.username,
                               password=self.password,
                               address=self.address)
        self.assertEqual(obj.username, self.username)
        self.assertEqual(obj.password, self.password)
        self.assertEqual(obj.address, self.address)

    def test_login(self):
        """Test login."""
        with HTTMock(content_login):
            res = requests.get('https://%s/LOGIN' % self.address)
        self.assertEqual(res.status_code, 200)

# -*- coding: utf-8 -*-

"""UnitTests for airwaveapiclient."""

import unittest
from httmock import all_requests, response, HTTMock
from airwaveapiclient import AirWaveAPIClient


class UnitTests(unittest.TestCase):

    """Class UnitTests.

    Unit test for airwaveapiclient.

    """

    def setUp(self):
        """Setup."""
        self.username = 'username'
        self.password = 'password'
        self.address = '192.168.1.1'
        self.obj = AirWaveAPIClient(username=self.username,
                                    password=self.password,
                                    address=self.address)

    def test_init(self):
        """Test init."""
        self.assertEqual(self.obj.username, self.username)
        self.assertEqual(self.obj.password, self.password)
        self.assertEqual(self.obj.address, self.address)

    def test_login(self):
        """Test login."""
        with HTTMock(UnitTests.content_login):
            res = self.obj.login()
        self.assertEqual(res.status_code, 200)

    # pylint: disable=unused-argument
    @staticmethod
    @all_requests
    def content_login(url, request):
        """Test content for login."""
        cookie_key = 'Mercury::Handler::AuthCookieHandler_AMPAuth'
        cookie_val = '01234567890abcdef01234567890abcd'
        headers = {'Set-Cookie': '%s=%s;' % (cookie_key, cookie_val)}
        content = '<html>html content.</html>'
        return response(status_code=200,
                        content=content,
                        headers=headers,
                        reason=None,
                        elapsed=5,
                        request=request)

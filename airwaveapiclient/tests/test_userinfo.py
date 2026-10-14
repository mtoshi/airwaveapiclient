# -*- coding: utf-8 -*-

"""UnitTests for UserInfo."""

import os
import unittest
from airwaveapiclient import UserInfo
from airwaveapiclient.tests import test_utils


class UserInfoUnitTests(unittest.TestCase):

    """Unit test for UserInfo."""

    def setUp(self):
        """Setup."""
        self.filename = 'test_userinfo.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.filename)
        self.xml_data = test_utils.read_file(path)
        self.obj = UserInfo(self.xml_data)

    def test_init(self):
        """Test init."""
        self.assertIsNotNone(self.obj)
        self.assertEqual(self.obj['@id'], '3')
        self.assertEqual(self.obj['username'], 'admin')
        self.assertEqual(self.obj['access_level'], 'admin')
        self.assertEqual(self.obj['rapids'], 'true')

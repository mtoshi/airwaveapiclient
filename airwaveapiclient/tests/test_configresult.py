# -*- coding: utf-8 -*-

"""UnitTests for ConfigResult."""

import os
import unittest
from airwaveapiclient import ConfigResult
from airwaveapiclient.tests import test_utils


class ConfigResultUnitTests(unittest.TestCase):

    """Class ConfigResultUnitTests.

    Unit test for ConfigResult.

    """

    def setUp(self):
        """Setup."""
        self.json_file = os.path.join(os.path.dirname(__file__), 'test_configresult.json')
        self.data = test_utils.read_file(self.json_file)
        self.obj = ConfigResult(self.data)

    def test_json_success(self):
        """Test JSON success output."""
        self.assertTrue(self.obj.success)
        self.assertIn('extraction successful', self.obj.status)
        self.assertEqual(self.obj['status'], self.obj.status)

    def test_text_device_deleted(self):
        """Test plain text device deleted output."""
        res = ConfigResult('Device is deleted successfully')
        self.assertTrue(res.success)
        self.assertEqual(res.message, 'Device is deleted successfully')

    def test_text_device_not_found(self):
        """Test plain text device does not exist output."""
        res = ConfigResult('Device does not exist')
        self.assertTrue(res.success)
        self.assertEqual(res.message, 'Device does not exist')

    def test_text_failure(self):
        """Test failure response."""
        res = ConfigResult('{"status": "PKCS bundle extraction failed."}')
        self.assertFalse(res.success)
        self.assertEqual(res.status, 'PKCS bundle extraction failed.')

    def test_dict_input(self):
        """Test dict input."""
        res = ConfigResult({'status': 'Device is moved to a folder successfully'})
        self.assertTrue(res.success)
        self.assertEqual(res.status, 'Device is moved to a folder successfully')

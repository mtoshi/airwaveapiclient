# -*- coding: utf-8 -*-

"""UnitTests for APLog."""

import os
import unittest
from airwaveapiclient import APLog
from airwaveapiclient.tests import test_utils


class APLogUnitTests(unittest.TestCase):

    """Unit test for APLog."""

    def setUp(self):
        """Setup."""
        self.filename = 'test_aplog.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.filename)
        self.xml_data = test_utils.read_file(path)
        self.obj = APLog(self.xml_data)

    def test_init(self):
        """Test init."""
        self.assertIsNotNone(self.obj)
        self.assertEqual(len(self.obj), 3)
        self.assertEqual(self.obj[0]['@ap_id'], '79')
        self.assertEqual(self.obj[0]['message'], 'AP Client Count: Device: ORiNOCO-AP-700-55-e6-e1: >= 1 clients for 15 seconds (Normal)')
        self.assertEqual(self.obj[0]['user'], 'System')

        self.assertEqual(self.obj[1]['@ap_id'], '79')
        self.assertEqual(self.obj[1]['message'], 'Configuration verification: configuration on device does not match desired configuration')

        self.assertEqual(self.obj[2]['@ap_id'], '80')
        self.assertEqual(self.obj[2]['message'], "Status changed to 'SNMP Get Failed'")
        self.assertEqual(self.obj[2]['user'], 'System')

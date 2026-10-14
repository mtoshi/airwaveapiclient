# -*- coding: utf-8 -*-

"""UnitTests for ClientLocation."""

import os
import unittest
from airwaveapiclient import ClientLocation
from airwaveapiclient.tests import test_utils


class ClientLocationUnitTests(unittest.TestCase):

    """Class ClientLocationUnitTests.

    Unit test for ClientLocation.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_clientlocation.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = ClientLocation(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(self.obj['@site_id'], 'f6cffbef-4a17-438b-97da-1a29de9d1802')
        self.assertEqual(self.obj['client']['@mac'], '12:34:56:78:90:AB')
        self.assertEqual(self.obj['client']['@x'], '120.5')
        self.assertEqual(self.obj['client']['@y'], '85.3')

# -*- coding: utf-8 -*-

"""UnitTests for AlertList."""

import os
import unittest
from airwaveapiclient import AlertList
from airwaveapiclient.tests import test_utils


class AlertListUnitTests(unittest.TestCase):

    """Unit test for AlertList."""

    def setUp(self):
        """Setup."""
        self.filename = 'test_alertlist.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.filename)
        self.xml_data = test_utils.read_file(path)
        self.obj = AlertList(self.xml_data)

    def test_init(self):
        """Test init."""
        self.assertIsNotNone(self.obj)
        self.assertEqual(len(self.obj), 2)
        self.assertEqual(self.obj[0]['@id'], '83')
        self.assertEqual(self.obj[1]['@id'], '84')

    def test_search(self):
        """Test search."""
        # Integer search
        alert = self.obj.search(83)
        self.assertIsNotNone(alert)
        self.assertEqual(alert['@id'], '83')
        self.assertEqual(alert['type']['#text'], 'Device Client Count')

        # String search
        alert_str = self.obj.search('84')
        self.assertIsNotNone(alert_str)
        self.assertEqual(alert_str['@id'], '84')

        # Non-existent ID
        self.assertIsNone(self.obj.search(999))

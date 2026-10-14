# -*- coding: utf-8 -*-

"""UnitTests for AMPStats."""

import os
import unittest
from airwaveapiclient import AMPStats
from airwaveapiclient.tests import test_utils


class AMPStatsUnitTests(unittest.TestCase):

    """Unit test for AMPStats."""

    def setUp(self):
        """Setup."""
        self.filename = 'test_ampstats.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.filename)
        self.xml_data = test_utils.read_file(path)
        self.obj = AMPStats(self.xml_data)

    def test_init(self):
        """Test init."""
        self.assertIsNotNone(self.obj)
        self.assertEqual(self.obj['up'], '25')
        self.assertEqual(self.obj['down'], '10')
        self.assertEqual(self.obj['client_count'], '120')
        self.assertEqual(self.obj['name'], 'AirWave Management Platform')
        self.assertEqual(self.obj['@console_refresh_rate'], '60')

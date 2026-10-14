# -*- coding: utf-8 -*-

"""UnitTests for Topology."""

import os
import unittest
from airwaveapiclient import Topology
from airwaveapiclient.tests import test_utils


class TopologyUnitTests(unittest.TestCase):

    """Class TopologyUnitTests.

    Unit test for Topology.

    """

    def setUp(self):
        """Setup."""
        self.json_file = os.path.join(os.path.dirname(__file__), 'test_topology.json')
        self.data = test_utils.read_file(self.json_file)
        self.obj = Topology(self.data)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj), 2)
        self.assertEqual(self.obj[0]['apID'], 31)
        self.assertEqual(self.obj[0]['name'], 'b4:5d:50:')
        self.assertEqual(self.obj[0]['folder']['name'], 'Top/Aruba HPE/SLR01')
        self.assertEqual(self.obj[1]['apID'], 230)
        self.assertEqual(self.obj[1]['HealthInfo']['health'], 'poor')

    def test_search_by_ap_id_int(self):
        """Test search by AP ID integer."""
        node = self.obj.search(31)
        self.assertIsNotNone(node)
        self.assertEqual(node['name'], 'b4:5d:50:')

    def test_search_by_ap_id_str(self):
        """Test search by AP ID string."""
        node = self.obj.search('230')
        self.assertIsNotNone(node)
        self.assertEqual(node['name'], 'SLR01-OUT-AP275')

    def test_search_by_name(self):
        """Test search by name."""
        node = self.obj.search('SLR01-OUT-AP275')
        self.assertIsNotNone(node)
        self.assertEqual(node['apID'], 230)

    def test_search_by_mac(self):
        """Test search by MAC address."""
        node = self.obj.search('B4:5D:50:00:00:01')
        self.assertIsNotNone(node)
        self.assertEqual(node['apID'], 31)

    def test_search_not_found(self):
        """Test search not found."""
        self.assertIsNone(self.obj.search(9999))
        self.assertIsNone(self.obj.search('nonexistent'))

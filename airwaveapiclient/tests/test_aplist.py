# -*- coding: utf-8 -*-

"""UnitTests for airwaveapiclient."""

import os
import unittest
from airwaveapiclient import APList
from airwaveapiclient.tests import test_utils


class APListUnitTests(unittest.TestCase):

    """Class APListUnitTests.

    Unit test for APList.

    """

    def setUp(self):
        """Setup."""
        self.ap_list_file = 'test_aplist.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.ap_list_file)
        self.ap_list = test_utils.read_file(path)
        self.obj = APList(self.ap_list)

    def tearDown(self):
        """Tear down."""

    def test_init(self):
        """Test init."""
        self.assertNotEqual(self.obj, None)

    def test_search(self):
        """Test search."""
        # ap_id integer search
        ap_id = 1
        ap_node = self.obj.search(ap_id)
        self.assertEqual(ap_node['@id'], '1')

        ap_id = 2
        ap_node = self.obj.search(ap_id)
        self.assertEqual(ap_node['@id'], '2')

        ap_id = 3
        ap_node = self.obj.search(ap_id)
        self.assertEqual(ap_node['@id'], '3')

        ap_id = 4
        ap_node = self.obj.search(ap_id)
        self.assertEqual(ap_node['@id'], '4')

        ap_id = 5
        ap_node = self.obj.search(ap_id)
        self.assertEqual(ap_node, None)

        # ap_name string search
        ap_name = 'AP001'
        ap_node = self.obj.search(ap_name)
        self.assertEqual(ap_node['name'], ap_name)

        ap_name = 'AP002'
        ap_node = self.obj.search(ap_name)
        self.assertEqual(ap_node['name'], ap_name)

        ap_name = 'AP003'
        ap_node = self.obj.search(ap_name)
        self.assertEqual(ap_node['name'], ap_name)

        ap_name = 'AP004'
        ap_node = self.obj.search(ap_name)
        self.assertEqual(ap_node['name'], ap_name)

        ap_name = 'AP005'
        ap_node = self.obj.search(ap_name)
        self.assertEqual(ap_node, None)

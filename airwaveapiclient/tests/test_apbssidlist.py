# -*- coding: utf-8 -*-

"""UnitTests for APBSSIDList."""

import os
import unittest
from airwaveapiclient import APBSSIDList
from airwaveapiclient.tests import test_utils


class APBSSIDListUnitTests(unittest.TestCase):

    """Unit test for APBSSIDList."""

    def setUp(self):
        """Setup."""
        self.filename = 'test_apbssidlist.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.filename)
        self.xml_data = test_utils.read_file(path)
        self.obj = APBSSIDList(self.xml_data)

    def test_init(self):
        """Test init."""
        self.assertIsNotNone(self.obj)
        self.assertEqual(len(self.obj), 2)

    def test_search(self):
        """Test search."""
        # Integer search by AP ID
        ap1 = self.obj.search(19251)
        self.assertIsNotNone(ap1)
        self.assertEqual(ap1['@id'], '19251')
        self.assertEqual(ap1['@name'], 'AP 1')

        # String search by AP name
        ap2 = self.obj.search('AP 2')
        self.assertIsNotNone(ap2)
        self.assertEqual(ap2['@id'], '19252')

        # Non-existent search
        self.assertIsNone(self.obj.search(999))

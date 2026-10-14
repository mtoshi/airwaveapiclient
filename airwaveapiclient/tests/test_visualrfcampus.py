# -*- coding: utf-8 -*-

"""UnitTests for VisualRFCampus."""

import os
import unittest
from airwaveapiclient import VisualRFCampus
from airwaveapiclient.tests import test_utils


class VisualRFCampusUnitTests(unittest.TestCase):

    """Class VisualRFCampusUnitTests.

    Unit test for VisualRFCampus.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_visualrfcampus.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = VisualRFCampus(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj), 2)
        self.assertEqual(self.obj[0]['@id'], '3')
        self.assertEqual(self.obj[0]['@name'], 'NorthEast')
        self.assertEqual(self.obj[1]['@id'], '4')
        self.assertEqual(self.obj[1]['@name'], 'WestCoast')

    def test_search_by_id(self):
        """Test search by campus ID."""
        campus = self.obj.search('3')
        self.assertIsNotNone(campus)
        self.assertEqual(campus['@name'], 'NorthEast')

    def test_search_by_name(self):
        """Test search by campus name."""
        campus = self.obj.search('WestCoast')
        self.assertIsNotNone(campus)
        self.assertEqual(campus['@id'], '4')

    def test_search_not_found(self):
        """Test search not found."""
        self.assertIsNone(self.obj.search('nonexistent'))

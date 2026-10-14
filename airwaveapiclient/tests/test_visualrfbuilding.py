# -*- coding: utf-8 -*-

"""UnitTests for VisualRFBuilding."""

import os
import unittest
from airwaveapiclient import VisualRFBuilding
from airwaveapiclient.tests import test_utils


class VisualRFBuildingUnitTests(unittest.TestCase):

    """Class VisualRFBuildingUnitTests.

    Unit test for VisualRFBuilding.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_visualrfbuilding.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = VisualRFBuilding(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj), 1)
        self.assertEqual(self.obj[0]['@id'], '15')
        self.assertEqual(self.obj[0]['@name'], 'NYC Office')
        self.assertEqual(self.obj[0]['@campus_id'], '3')

    def test_search_by_id(self):
        """Test search by building ID."""
        b = self.obj.search('15')
        self.assertIsNotNone(b)
        self.assertEqual(b['@name'], 'NYC Office')

    def test_search_by_name(self):
        """Test search by building name."""
        b = self.obj.search('NYC Office')
        self.assertIsNotNone(b)
        self.assertEqual(b['@id'], '15')

    def test_search_not_found(self):
        """Test search not found."""
        self.assertIsNone(self.obj.search('nonexistent'))

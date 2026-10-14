# -*- coding: utf-8 -*-

"""UnitTests for VisualRFSite."""

import os
import unittest
from airwaveapiclient import VisualRFSite
from airwaveapiclient.tests import test_utils


class VisualRFSiteUnitTests(unittest.TestCase):

    """Class VisualRFSiteUnitTests.

    Unit test for VisualRFSite.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_visualrfsite.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = VisualRFSite(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj), 1)
        self.assertEqual(self.obj[0]['@id'], 'f6cffbef-4a17-438b-97da-1a29de9d1802')
        self.assertEqual(self.obj[0]['@name'], 'Office')
        self.assertEqual(self.obj[0]['@floor'], '1.0')

    def test_search_by_id(self):
        """Test search by site ID."""
        s = self.obj.search('f6cffbef-4a17-438b-97da-1a29de9d1802')
        self.assertIsNotNone(s)
        self.assertEqual(s['@name'], 'Office')

    def test_search_by_name(self):
        """Test search by site name."""
        s = self.obj.search('Office')
        self.assertIsNotNone(s)
        self.assertEqual(s['@id'], 'f6cffbef-4a17-438b-97da-1a29de9d1802')

    def test_search_not_found(self):
        """Test search not found."""
        self.assertIsNone(self.obj.search('nonexistent'))

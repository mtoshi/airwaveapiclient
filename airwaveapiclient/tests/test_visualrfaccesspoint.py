# -*- coding: utf-8 -*-

"""UnitTests for VisualRFAccessPoint."""

import os
import unittest
from airwaveapiclient import VisualRFAccessPoint
from airwaveapiclient.tests import test_utils


class VisualRFAccessPointUnitTests(unittest.TestCase):

    """Class VisualRFAccessPointUnitTests.

    Unit test for VisualRFAccessPoint.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_visualrfaccesspoint.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = VisualRFAccessPoint(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj), 1)
        self.assertEqual(self.obj[0]['@id'], '12660')
        self.assertEqual(self.obj[0]['@name'], 'Tropos Mesh Node 49842')
        self.assertEqual(self.obj[0]['@status'], 'down')

    def test_search_by_id(self):
        """Test search by AP ID."""
        ap = self.obj.search('12660')
        self.assertIsNotNone(ap)
        self.assertEqual(ap['@name'], 'Tropos Mesh Node 49842')

    def test_search_by_name(self):
        """Test search by AP name."""
        ap = self.obj.search('Tropos Mesh Node 49842')
        self.assertIsNotNone(ap)
        self.assertEqual(ap['@id'], '12660')

    def test_search_not_found(self):
        """Test search not found."""
        self.assertIsNone(self.obj.search('nonexistent'))

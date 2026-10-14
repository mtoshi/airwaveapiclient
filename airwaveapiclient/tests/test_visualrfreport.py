# -*- coding: utf-8 -*-

"""UnitTests for VisualRFReport."""

import os
import unittest
from airwaveapiclient import VisualRFReport
from airwaveapiclient.tests import test_utils


class VisualRFReportUnitTests(unittest.TestCase):

    """Class VisualRFReportUnitTests.

    Unit test for VisualRFReport.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_visualrfreport.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = VisualRFReport(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj), 1)
        self.assertEqual(self.obj[0]['@id'], '71c1057b-1771-4b56-a955-ce6514e8f703')
        self.assertEqual(self.obj[0]['@name'], 'BOM Report')

    def test_search_by_id(self):
        """Test search by report ID."""
        r = self.obj.search('71c1057b-1771-4b56-a955-ce6514e8f703')
        self.assertIsNotNone(r)
        self.assertEqual(r['@name'], 'BOM Report')

    def test_search_by_name(self):
        """Test search by report name."""
        r = self.obj.search('BOM Report')
        self.assertIsNotNone(r)
        self.assertEqual(r['@id'], '71c1057b-1771-4b56-a955-ce6514e8f703')

    def test_search_not_found(self):
        """Test search not found."""
        self.assertIsNone(self.obj.search('nonexistent'))

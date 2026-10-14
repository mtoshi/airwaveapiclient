# -*- coding: utf-8 -*-

"""UnitTests for APSearch."""

import os
import unittest
from airwaveapiclient import APSearch
from airwaveapiclient.tests import test_utils


class APSearchUnitTests(unittest.TestCase):

    """Class APSearchUnitTests.

    Unit test for APSearch.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_apsearch.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = APSearch(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj), 2)
        self.assertEqual(self.obj[0]['@id'], '3647')
        self.assertEqual(self.obj[0]['name']['#text'], 'ap:1b:a6:90')

    def test_search_by_id(self):
        """Test search by record ID."""
        rec = self.obj.search('3647')
        self.assertIsNotNone(rec)
        self.assertEqual(rec['name']['#text'], 'ap:1b:a6:90')

    def test_search_by_name(self):
        """Test search by name."""
        rec = self.obj.search('ap:1b:a6:91')
        self.assertIsNotNone(rec)
        self.assertEqual(rec['@id'], '3648')

    def test_search_not_found(self):
        """Test search not found."""
        self.assertIsNone(self.obj.search('unknown'))

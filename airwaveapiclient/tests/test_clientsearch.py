# -*- coding: utf-8 -*-

"""UnitTests for ClientSearch."""

import os
import unittest
from airwaveapiclient import ClientSearch
from airwaveapiclient.tests import test_utils


class ClientSearchUnitTests(unittest.TestCase):

    """Class ClientSearchUnitTests.

    Unit test for ClientSearch.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_clientsearch.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = ClientSearch(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj), 1)
        self.assertEqual(self.obj[0]['@id'], '310')
        self.assertEqual(self.obj[0]['mac']['#text'], '00:0E:35:52:8C:AB')
        self.assertEqual(self.obj[0]['username']['#text'], 'packplane')

    def test_search_by_id(self):
        """Test search by record ID."""
        rec = self.obj.search('310')
        self.assertIsNotNone(rec)
        self.assertEqual(rec['username']['#text'], 'packplane')

    def test_search_by_mac(self):
        """Test search by MAC address."""
        rec = self.obj.search('00:0E:35:52:8C:AB')
        self.assertIsNotNone(rec)
        self.assertEqual(rec['@id'], '310')

    def test_search_by_username(self):
        """Test search by username."""
        rec = self.obj.search('packplane')
        self.assertIsNotNone(rec)
        self.assertEqual(rec['@id'], '310')

    def test_search_not_found(self):
        """Test search not found."""
        self.assertIsNone(self.obj.search('nonexistent'))

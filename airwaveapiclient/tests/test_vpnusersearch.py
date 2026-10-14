# -*- coding: utf-8 -*-

"""UnitTests for VPNUserSearch."""

import os
import unittest
from airwaveapiclient import VPNUserSearch
from airwaveapiclient.tests import test_utils


class VPNUserSearchUnitTests(unittest.TestCase):

    """Class VPNUserSearchUnitTests.

    Unit test for VPNUserSearch.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_vpnusersearch.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = VPNUserSearch(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj), 1)
        self.assertEqual(self.obj[0]['@id'], '310')
        self.assertEqual(self.obj[0]['userid']['#text'], 'photocrayon')
        self.assertEqual(self.obj[0]['session_count']['#text'], '1')

    def test_search_by_id(self):
        """Test search by record ID."""
        rec = self.obj.search('310')
        self.assertIsNotNone(rec)
        self.assertEqual(rec['userid']['#text'], 'photocrayon')

    def test_search_by_userid(self):
        """Test search by userid."""
        rec = self.obj.search('photocrayon')
        self.assertIsNotNone(rec)
        self.assertEqual(rec['@id'], '310')

    def test_search_not_found(self):
        """Test search not found."""
        self.assertIsNone(self.obj.search('unknown_user'))

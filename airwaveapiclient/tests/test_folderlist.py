# -*- coding: utf-8 -*-

"""UnitTests for FolderList."""

import os
import unittest
from airwaveapiclient import FolderList
from airwaveapiclient.tests import test_utils


class FolderListUnitTests(unittest.TestCase):

    """Class FolderListUnitTests.

    Unit test for FolderList.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_folderlist.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = FolderList(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj), 2)
        self.assertEqual(self.obj[0]['name'], 'Top')
        self.assertEqual(self.obj[1]['name'], 'Branch Office')

    def test_search_by_id_int(self):
        """Test search by folder ID integer."""
        folder = self.obj.search(1)
        self.assertIsNotNone(folder)
        self.assertEqual(folder['name'], 'Top')

    def test_search_by_id_str(self):
        """Test search by folder ID string."""
        folder = self.obj.search('2')
        self.assertIsNotNone(folder)
        self.assertEqual(folder['name'], 'Branch Office')

    def test_search_not_found(self):
        """Test search not found."""
        self.assertIsNone(self.obj.search(999))
        self.assertIsNone(self.obj.search('nonexistent'))

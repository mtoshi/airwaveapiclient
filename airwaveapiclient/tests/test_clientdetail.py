# -*- coding: utf-8 -*-

"""UnitTests for ClientDetail."""

import os
import unittest
from airwaveapiclient import ClientDetail
from airwaveapiclient.tests import test_utils


class ClientDetailUnitTests(unittest.TestCase):

    """Unit test for ClientDetail."""

    def setUp(self):
        """Setup."""
        self.filename = 'test_clientdetail.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.filename)
        self.xml_data = test_utils.read_file(path)
        self.obj = ClientDetail(self.xml_data)

    def test_init(self):
        """Test init."""
        self.assertIsNotNone(self.obj)
        self.assertEqual(self.obj['@mac'], '00:0E:35:52:8C:AB')
        self.assertEqual(self.obj['rssi'], '36')
        self.assertEqual(self.obj['vendor'], 'Intel')
        self.assertEqual(self.obj['role'], 'Employee')
        self.assertEqual(len(self.obj.clients), 1)

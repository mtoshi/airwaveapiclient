# -*- coding: utf-8 -*-

"""UnitTests for airwaveapiclient."""

import os
import unittest
from airwaveapiclient import APDetail
from airwaveapiclient.tests import test_utils


class APDetailUnitTests(unittest.TestCase):

    """Class APDetailUnitTests.

    Unit test for APDetail.

    """

    def setUp(self):
        """Setup."""
        self.ap_detail_file = 'test_apdetail.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.ap_detail_file)
        self.ap_detail = test_utils.read_file(path)
        self.obj = APDetail(self.ap_detail)

    def tearDown(self):
        """Tear down."""

    def test_init(self):
        """Test init."""
        self.assertNotEqual(self.obj, None)

    def test_radio_type(self):
        """Test radio_type."""
        for radio in self.obj['radio']:
            if radio['radio_type'] == 'bgn':
                self.assertEqual(radio['radio_interface'], '2')
            if radio['radio_type'] == 'aN':
                self.assertEqual(radio['radio_interface'], '1')

    def test_multi_ap(self):
        """Test multi-AP XML response in APDetail."""
        multi_xml = """<?xml version="1.0" encoding="utf-8"?>
        <amp:amp_ap_detail xmlns:amp="http://www.airwave.com" version="1">
          <ap id="1">
            <name>AP001</name>
          </ap>
          <ap id="2">
            <name>AP002</name>
          </ap>
        </amp:amp_ap_detail>"""
        multi_obj = APDetail(multi_xml)
        self.assertEqual(len(multi_obj.aps), 2)
        self.assertEqual(multi_obj.aps[0]['@id'], '1')
        self.assertEqual(multi_obj.aps[0]['name'], 'AP001')
        self.assertEqual(multi_obj.aps[1]['@id'], '2')
        self.assertEqual(multi_obj.aps[1]['name'], 'AP002')
        # Backward-compatible first AP dictionary access
        self.assertEqual(multi_obj['@id'], '1')
        self.assertEqual(multi_obj['name'], 'AP001')

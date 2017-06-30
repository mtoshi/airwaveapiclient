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

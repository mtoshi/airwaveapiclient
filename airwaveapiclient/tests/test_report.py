# -*- coding: utf-8 -*-

"""UnitTests for report."""

import os
import unittest
from airwaveapiclient import Report
from airwaveapiclient.tests import test_utils


class ReportUnitTests(unittest.TestCase):

    """Class ReportUnitTests.

    Unit test for Report.

    """

    def setUp(self):
        """Setup."""
        self.report_file = 'test_report.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.report_file)
        self.ap_list = test_utils.read_file(path)
        self.obj = Report(self.ap_list)

    def tearDown(self):
        """Tear down."""

    def test_init(self):
        """Test init."""
        self.assertNotEqual(self.obj, None)
        self.assertEqual(type(self.obj), Report)
        self.assertEqual(len(self.obj['pickled_ap_summary']), 3)
        self.assertEqual(len(self.obj['pickled_rf_health']), 6)

# -*- coding: utf-8 -*-

"""UnitTests for RogueDetail."""

import os
import unittest
from airwaveapiclient import RogueDetail
from airwaveapiclient.tests import test_utils


class RogueDetailUnitTests(unittest.TestCase):

    """Class RogueDetailUnitTests.

    Unit test for RogueDetail.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_roguedetail.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = RogueDetail(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(self.obj['@id'], '495')
        self.assertEqual(self.obj['channel'], '6')
        self.assertEqual(self.obj['discovery_event']['@id'], '600644')
        self.assertEqual(self.obj['discovery_event']['signal'], '70')

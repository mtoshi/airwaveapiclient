# -*- coding: utf-8 -*-

"""UnitTests for VisualRFRasterize."""

import os
import unittest
from airwaveapiclient import VisualRFRasterize
from airwaveapiclient.tests import test_utils


class VisualRFRasterizeUnitTests(unittest.TestCase):

    """Class VisualRFRasterizeUnitTests.

    Unit test for VisualRFRasterize.

    """

    def setUp(self):
        """Setup."""
        self.xml_file = os.path.join(os.path.dirname(__file__), 'test_visualrfrasterize.xml')
        self.xml = test_utils.read_file(self.xml_file)
        self.obj = VisualRFRasterize(self.xml)

    def test_init(self):
        """Test init."""
        self.assertEqual(len(self.obj.images), 1)
        self.assertEqual(self.obj.images[0]['@type'], 'raster')
        self.assertEqual(self.obj.images[0]['pixel-width'], '400')
        self.assertEqual(self.obj.images[0]['file-size'], '20544')

    def test_sites_response(self):
        """Test sites response for rasterize stats."""
        xml_sites = """<?xml version="1.0" encoding="UTF-8"?>
        <visualrf:sites xmlns:visualrf="http://www.airwave.com" version="1">
          <site building_id="b1" building_name="Building 1" id="s1" name="Floor 1"/>
        </visualrf:sites>"""
        raster = VisualRFRasterize(xml_sites)
        self.assertEqual(len(raster.sites), 1)
        self.assertEqual(raster.sites[0]['@id'], 's1')
        self.assertEqual(raster.sites[0]['@name'], 'Floor 1')

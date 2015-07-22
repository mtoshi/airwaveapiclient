# -*- coding: utf-8 -*-

"""UnitTests for ap_graph."""

import unittest
from airwaveapiclient import APGraph
from airwaveapiclient import APList
from airwaveapiclient.tests import test_utils
import os


class APGraphUnitTests(unittest.TestCase):

    """Class APGraphUnitTests.

    Unit test for APGraph.

    """

    def setUp(self):
        """Setup."""
        self.url = u'https://192.168.1.1/'
        self.ap_list_file = 'test_ap_list.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.ap_list_file)
        self.ap_list = test_utils.read_file(path)
        self.objs = APList(self.ap_list)

    def tearDown(self):
        """Tear down."""

    def test_init(self):
        """Test init."""
        ap_graph = APGraph(self.url, self.objs[0])
        self.assertEqual(ap_graph.url, u'https://192.168.1.1/')
        self.assertEqual(ap_graph.path, u'/nf/rrd_graph')
        self.assertEqual(ap_graph.default_start_time, -7200)
        self.assertEqual(ap_graph.default_end_time, 0)

        ap_graph = APGraph(self.url, self.objs[1])
        self.assertEqual(ap_graph.url, u'https://192.168.1.1/')
        self.assertEqual(ap_graph.path, u'/nf/rrd_graph')
        self.assertEqual(ap_graph.default_start_time, -7200)
        self.assertEqual(ap_graph.default_end_time, 0)

        ap_graph = APGraph(self.url, self.objs[2])
        self.assertEqual(ap_graph.url, u'https://192.168.1.1/')
        self.assertEqual(ap_graph.path, u'/nf/rrd_graph')
        self.assertEqual(ap_graph.default_start_time, -7200)
        self.assertEqual(ap_graph.default_end_time, 0)

    def test_client_count_802dot11bgn(self):
        """Test for client_count_802dot11bgn."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.client_count_802dot11bgn()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'end=0s&'
                      'id=1&'
                      'radio_index=1&'
                      'start=-7200s&'
                      'type=ap_client_count')
        self.assertEqual(graph_url, _graph_url)

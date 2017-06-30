# -*- coding: utf-8 -*-

"""UnitTests for ap_graph."""

import os
import unittest
from airwaveapiclient import APGraph
from airwaveapiclient import APList
from airwaveapiclient.tests import test_utils


class APGraphUnitTests(unittest.TestCase):

    """Class APGraphUnitTests.

    Unit test for APGraph.

    """

    def setUp(self):
        """Setup."""
        self.url = u'https://192.168.1.1/'
        self.ap_list_file = 'test_aplist.xml'
        self.here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(self.here, self.ap_list_file)
        self.ap_list = test_utils.read_file(path)
        self.objs = APList(self.ap_list)

    def tearDown(self):
        """Tear down."""

    def test_init(self):
        """Test init."""
        # 802.11bgn, 802.11an
        ap_graph = APGraph(self.url, self.objs[0])
        self.assertEqual(ap_graph.url, u'https://192.168.1.1/')
        self.assertEqual(ap_graph.path, u'/nf/rrd_graph')
        self.assertEqual(ap_graph.default_start_time, -7200)
        self.assertEqual(ap_graph.default_end_time, 0)

        # 802.11bgn, 802.11an
        ap_graph = APGraph(self.url, self.objs[1])
        self.assertEqual(ap_graph.url, u'https://192.168.1.1/')
        self.assertEqual(ap_graph.path, u'/nf/rrd_graph')
        self.assertEqual(ap_graph.default_start_time, -7200)
        self.assertEqual(ap_graph.default_end_time, 0)

        # 802.11bgn, 802.11ac
        ap_graph = APGraph(self.url, self.objs[2])
        self.assertEqual(ap_graph.url, u'https://192.168.1.1/')
        self.assertEqual(ap_graph.path, u'/nf/rrd_graph')
        self.assertEqual(ap_graph.default_start_time, -7200)
        self.assertEqual(ap_graph.default_end_time, 0)

        # 802.11bgn only
        ap_graph = APGraph(self.url, self.objs[3])
        self.assertEqual(ap_graph.url, u'https://192.168.1.1/')
        self.assertEqual(ap_graph.path, u'/nf/rrd_graph')
        self.assertEqual(ap_graph.default_start_time, -7200)
        self.assertEqual(ap_graph.default_end_time, 0)

    # pylint: disable=protected-access
    def test_graph_url(self):
        """Test Graph URL."""
        params = {u'aaa': u''}
        ap_graph = APGraph(self.url, self.objs[0])
        url = ap_graph._APGraph__graph_url(params)
        self.assertEqual(url, None)

        params = {u'radio_index': u'',
                  u'start': u'',
                  u'end': u''}
        ap_graph = APGraph(self.url, self.objs[0])
        url = ap_graph._APGraph__graph_url(params)
        _url = (u'https://192.168.1.1/nf/rrd_graph?'
                u'end=0s&radio_index=&start=-7200s')
        self.assertEqual(url, _url)

        ap_graph = APGraph(self.url, self.objs[3])
        url = ap_graph._APGraph__graph_url(params)
        _url = (u'https://192.168.1.1/nf/rrd_graph?'
                u'end=0s&radio_index=&start=-7200s')
        self.assertEqual(url, _url)

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

    def test_client_count_802dot11an(self):
        """Test for client_count_802dot11an."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.client_count_802dot11an()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'end=0s&'
                      'id=1&'
                      'radio_index=2&'
                      'start=-7200s&'
                      'type=ap_client_count')
        self.assertEqual(graph_url, _graph_url)

    def test_client_count_802dot11ac(self):
        """Test for client_count_802dot11ac."""
        ap_graph = APGraph(self.url, self.objs[2])
        graph_url = ap_graph.client_count_802dot11ac()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'end=0s&'
                      'id=3&'
                      'radio_index=2&'
                      'start=-7200s&'
                      'type=ap_client_count')
        self.assertEqual(graph_url, _graph_url)

        # For does not have 802.11ac
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.client_count_802dot11ac()
        self.assertEqual(graph_url, None)

    def test_bandwidth_802dot11bgn(self):
        """Test for bandwidth 802dot11bgn."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.bandwidth_802dot11bgn()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'end=0s&'
                      'id=1&'
                      'radio_index=1&'
                      'start=-7200s&'
                      'type=ap_bandwidth')
        self.assertEqual(graph_url, _graph_url)

    def test_bandwidth_802dot11an(self):
        """Test for bandwidth 802dot11an."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.bandwidth_802dot11an()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'end=0s&'
                      'id=1&'
                      'radio_index=2&'
                      'start=-7200s&'
                      'type=ap_bandwidth')
        self.assertEqual(graph_url, _graph_url)

    def test_bandwidth_802dot11ac(self):
        """Test for bandwidth 802dot11ac."""
        ap_graph = APGraph(self.url, self.objs[2])
        graph_url = ap_graph.bandwidth_802dot11ac()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'end=0s&'
                      'id=3&'
                      'radio_index=2&'
                      'start=-7200s&'
                      'type=ap_bandwidth')
        self.assertEqual(graph_url, _graph_url)

        # For does not have 802.11ac
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.bandwidth_802dot11ac()
        self.assertEqual(graph_url, None)

    def test_dot11_counters_802dot11bgn(self):
        """Test for dot11 counters 802dot11bgn."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.dot11_counters_802dot11bgn()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'end=0s&'
                      'id=1&'
                      'radio_index=1&'
                      'start=-7200s&'
                      'type=dot11_counters')
        self.assertEqual(graph_url, _graph_url)

    def test_dot11_counters_802dot11an(self):
        """Test for dot11 counters 802dot11an."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.dot11_counters_802dot11an()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'end=0s&'
                      'id=1&'
                      'radio_index=2&'
                      'start=-7200s&'
                      'type=dot11_counters')
        self.assertEqual(graph_url, _graph_url)

    def test_dot11_counters_802dot11ac(self):
        """Test for dot11 counters 802dot11ac."""
        ap_graph = APGraph(self.url, self.objs[2])
        graph_url = ap_graph.dot11_counters_802dot11ac()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'end=0s&'
                      'id=3&'
                      'radio_index=2&'
                      'start=-7200s&'
                      'type=dot11_counters')
        self.assertEqual(graph_url, _graph_url)

        # For does not have 802.11ac
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.dot11_counters_802dot11ac()
        self.assertEqual(graph_url, None)

    def test_radio_channel_802dot11bgn(self):
        """Test for channel 802dot11bgn."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_channel_802dot11bgn()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=1&'
                      'radio_interface=2&'
                      'start=-7200s&'
                      'type=radio_channel')
        self.assertEqual(graph_url, _graph_url)

    def test_radio_channel_802dot11an(self):
        """Test for channel 802dot11an."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_channel_802dot11an()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=radio_channel')
        self.assertEqual(graph_url, _graph_url)

    def test_radio_channel_802dot11ac(self):
        """Test for channel 802dot11ac."""
        ap_graph = APGraph(self.url, self.objs[2])
        graph_url = ap_graph.radio_channel_802dot11ac()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A03&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=radio_channel')
        self.assertEqual(graph_url, _graph_url)

        # For does not have 802.11ac
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_channel_802dot11ac()
        self.assertEqual(graph_url, None)

    def test_radio_noise_802dot11bgn(self):
        """Test for radio noise 802dot11bgn."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_noise_802dot11bgn()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=1&'
                      'radio_interface=2&'
                      'start=-7200s&'
                      'type=radio_noise')
        self.assertEqual(graph_url, _graph_url)

    def test_radio_noise_802dot11an(self):
        """Test for radio noise 802dot11an."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_noise_802dot11an()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=radio_noise')
        self.assertEqual(graph_url, _graph_url)

    def test_radio_noise_802dot11ac(self):
        """Test for radio noise 802dot11ac."""
        ap_graph = APGraph(self.url, self.objs[2])
        graph_url = ap_graph.radio_noise_802dot11ac()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A03&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=radio_noise')
        self.assertEqual(graph_url, _graph_url)

        # For does not have 802.11ac
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_noise_802dot11ac()
        self.assertEqual(graph_url, None)

    def test_radio_power_802dot11bgn(self):
        """Test for radio power 802dot11bgn."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_power_802dot11bgn()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=1&'
                      'radio_interface=2&'
                      'start=-7200s&'
                      'type=radio_power')
        self.assertEqual(graph_url, _graph_url)

    def test_radio_power_802dot11an(self):
        """Test for radio power 802dot11an."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_power_802dot11an()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=radio_power')
        self.assertEqual(graph_url, _graph_url)

    def test_radio_power_802dot11ac(self):
        """Test for radio power 802dot11ac."""
        ap_graph = APGraph(self.url, self.objs[2])
        graph_url = ap_graph.radio_power_802dot11ac()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A03&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=radio_power')
        self.assertEqual(graph_url, _graph_url)

        # For does not have 802.11ac
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_power_802dot11ac()
        self.assertEqual(graph_url, None)

    def test_radio_errors_802dot11bgn(self):
        """Test for radio errors 802dot11bgn."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_errors_802dot11bgn()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=1&'
                      'radio_interface=2&'
                      'start=-7200s&'
                      'type=radio_errors')
        self.assertEqual(graph_url, _graph_url)

    def test_radio_errors_802dot11an(self):
        """Test for radio errors 802dot11an."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_errors_802dot11an()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=radio_errors')
        self.assertEqual(graph_url, _graph_url)

    def test_radio_errors_802dot11ac(self):
        """Test for radio errors 802dot11ac."""
        ap_graph = APGraph(self.url, self.objs[2])
        graph_url = ap_graph.radio_errors_802dot11ac()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A03&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=radio_errors')
        self.assertEqual(graph_url, _graph_url)

        # For does not have 802.11ac
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_errors_802dot11ac()
        self.assertEqual(graph_url, None)

    def test_radio_goodput_802dot11bgn(self):
        """Test for radio goodput 802dot11bgn."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_goodput_802dot11bgn()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=1&'
                      'radio_interface=2&'
                      'start=-7200s&'
                      'type=radio_goodput')
        self.assertEqual(graph_url, _graph_url)

    def test_radio_goodput_802dot11an(self):
        """Test for radio goodput 802dot11an."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_goodput_802dot11an()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=radio_goodput')
        self.assertEqual(graph_url, _graph_url)

    def test_radio_goodput_802dot11ac(self):
        """Test for radio goodput 802dot11ac."""
        ap_graph = APGraph(self.url, self.objs[2])
        graph_url = ap_graph.radio_goodput_802dot11ac()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A03&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=radio_goodput')
        self.assertEqual(graph_url, _graph_url)

        # For does not have 802.11ac
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.radio_goodput_802dot11ac()
        self.assertEqual(graph_url, None)

    def test_channel_utilization_802dot11bgn(self):
        """Test for channel utilization 802dot11bgn."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.channel_utilization_802dot11bgn()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=1&'
                      'radio_interface=2&'
                      'start=-7200s&'
                      'type=channel_utilization')
        self.assertEqual(graph_url, _graph_url)

    def test_channel_utilization_802dot11an(self):
        """Test for channel utilization 802dot11an."""
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.channel_utilization_802dot11an()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A01&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=channel_utilization')
        self.assertEqual(graph_url, _graph_url)

    def test_channel_utilization_802dot11ac(self):
        """Test for channel utilization 802dot11ac."""
        ap_graph = APGraph(self.url, self.objs[2])
        graph_url = ap_graph.channel_utilization_802dot11ac()
        _graph_url = ('https://192.168.1.1/nf/rrd_graph?'
                      'ap_uid=00%3A00%3A10%3A00%3A00%3A03&'
                      'end=0s&'
                      'radio_index=2&'
                      'radio_interface=1&'
                      'start=-7200s&'
                      'type=channel_utilization')
        self.assertEqual(graph_url, _graph_url)

        # For does not have 802.11ac
        ap_graph = APGraph(self.url, self.objs[0])
        graph_url = ap_graph.channel_utilization_802dot11ac()
        self.assertEqual(graph_url, None)

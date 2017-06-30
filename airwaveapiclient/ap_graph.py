# -*- coding: utf-8 -*-

"""airwaveapiclient.ap_graph"""


import re
from collections import OrderedDict
import requests
from requests.compat import urljoin


class APGraph(OrderedDict):

    """Aruba networks AirWave Graph.

    Attributes:

        :url (str): AirWave URL.
        :path (str): Graph path.
        :default_start_time(int): Graph start default time.
        :default_end_time(int): Graph end default time.

    """

    def __init__(self, url, obj):
        """Initialize AirWaveAPIClient.

        Args:

            :url (str): AirWave URL.
            :obj (collections.OrderedDict): APList element.

        Usage: ::

            >>> from airwaveapiclient import AirWaveAPIClient
            >>> from airwaveapiclient import APGraph
            >>> from airwaveapiclient import APList
            >>>
            >>> url = 'http://192.168.1.1/'
            >>>
            >>> airwave = AirWaveAPIClient(username='admin',
            >>>                            password='xxxxx',
            >>>                            url=url)
            >>>
            >>> airwave.login()
            >>> ap_list = airwave.ap_list()
            >>>
            >>> objs = APList(ap_list)
            >>> for obj in objs:
            ...     ap_graph = APGraph(url, obj)
            ...     ap_graph.client_count_802dot11an()
            ...
            'http://x.x.x.x/nf/rrd_graph?
                end=0s&id=1&radio_index=2&start=-7200s&type=ap_client_count'
            'http://x.x.x.x/nf/rrd_graph?
                end=0s&id=2&radio_index=2&start=-7200s&type=ap_client_count'
            'http://x.x.x.x/nf/rrd_graph?
                end=0s&id=3&radio_index=2&start=-7200s&type=ap_client_count'
            >>> airwave.logout()

        """
        self.url = url
        self.path = '/nf/rrd_graph'
        self.default_start_time = -7200
        self.default_end_time = 0
        OrderedDict.__init__(self, obj)

    def __graph_url(self, params):
        """RRD Graph URL."""
        if 'radio_index' in params:
            start = params['start']
            if not start:
                start = self.default_start_time

            end = params['end']
            if not end:
                end = self.default_end_time

            params['start'] = APGraph.graph_time_format(start)
            params['end'] = APGraph.graph_time_format(end)

            params = APGraph.urlencode(params)
            path = urljoin(self.url, self.path)
            return u'%s?%s' % (path, params)
        return None

    def __ap_graph(self, graph_type, radio_type, start, end):
        """RRD access point graph base method.

        Args:

            :graph_type (str): Graph type.
            :radio_type (str): Radio type.
            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        """
        params = {}
        params['type'] = graph_type
        params['id'] = self['@id']
        if 'radio' in self:
            radios = self['radio']
            if not isinstance(radios, list):
                radios = [radios]
            for radio in radios:
                if 'radio_type' in radio:
                    if radio['radio_type'] == radio_type:
                        params['radio_index'] = radio['@index']
                        params['start'] = start
                        params['end'] = end
                        return self.__graph_url(params)
        return None

    def client_count_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for access point client count of radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.client_count_802dot11bgn(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=1&radio_index=1&start=-3600s&type=ap_client_count'

        """
        return self.__ap_graph(u'ap_client_count', u'bgn', start, end)

    def client_count_802dot11an(self, start=None, end=None):
        """RRD graph URL for access point client count of radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.client_count_802dot11an(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=1&radio_index=2&start=-3600s&type=ap_client_count'

        """
        return self.__ap_graph(u'ap_client_count', u'aN', start, end)

    def client_count_802dot11ac(self, start=None, end=None):
        """RRD graph URL for access point client count of radio type IEEE802.11AC.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.client_count_802dot11ac(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=1&radio_index=2&start=-3600s&type=ap_client_count'

        """
        return self.__ap_graph(u'ap_client_count', u'ac', start, end)

    def bandwidth_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for access point bandwidth of radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.bandwidth_802dot11bgn(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=1&radio_index=1&start=-3600s&type=ap_bandwidth'

        """
        return self.__ap_graph(u'ap_bandwidth', u'bgn', start, end)

    def bandwidth_802dot11an(self, start=None, end=None):
        """RRD graph URL for access point bandwidth of radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.bandwidth_802dot11an(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=1&radio_index=2&start=-3600s&type=ap_bandwidth'

        """
        return self.__ap_graph(u'ap_bandwidth', u'aN', start, end)

    def bandwidth_802dot11ac(self, start=None, end=None):
        """RRD graph URL for access point bandwidth of radio type IEEE802.11AC.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.bandwidth_802dot11ac(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=3&radio_index=2&start=-3600s&type=ap_bandwidth'

        """
        return self.__ap_graph(u'ap_bandwidth', u'ac', start, end)

    def dot11_counters_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for access point dot11 counters of radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.dot11_counters_802dot11bgn(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=1&radio_index=1&start=-3600s&type=dot11_counters'

        """
        return self.__ap_graph(u'dot11_counters', u'bgn', start, end)

    def dot11_counters_802dot11an(self, start=None, end=None):
        """RRD graph URL for access point dot11 counters of radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.dot11_counters_802dot11an(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=1&radio_index=2&start=-3600s&type=dot11_counters'

        """
        return self.__ap_graph(u'dot11_counters', u'aN', start, end)

    def dot11_counters_802dot11ac(self, start=None, end=None):
        """RRD graph URL for access point dot11 counters of radio type IEEE802.11AC.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.dot11_counters_802dot11ac(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=3&radio_index=2&start=-3600s&type=dot11_counters'

        """
        return self.__ap_graph(u'dot11_counters', u'ac', start, end)

    def __radio_graph(self, graph_type, radio_type, start, end):
        """RRD access point graph base method.

        Args:

            :graph_type (str): Graph type.
            :radio_type (str): Radio type.
            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        """
        params = {}
        params['type'] = graph_type
        params['ap_uid'] = self['lan_mac']
        if 'radio' in self:
            radios = self['radio']
            if not isinstance(radios, list):
                radios = [radios]
            for radio in radios:
                if 'radio_type' in radio:
                    if radio['radio_type'] == radio_type:
                        params['radio_index'] = radio['@index']
                        params['radio_interface'] = radio['radio_interface']
                        params['start'] = start
                        params['end'] = end
                        return self.__graph_url(params)
        return None

    def radio_channel_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for radio channel for radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_channel_802dot11bgn(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=1&radio_interface=2&start=-3600s&type=radio_channel'

        """
        return self.__radio_graph(u'radio_channel', u'bgn', start, end)

    def radio_channel_802dot11an(self, start=None, end=None):
        """RRD graph URL for radio channel for radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_channel_802dot11an(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=1&start=-3600s&type=radio_channel'

        """
        return self.__radio_graph(u'radio_channel', u'aN', start, end)

    def radio_channel_802dot11ac(self, start=None, end=None):
        """RRD graph URL for radio channel for radio type IEEE802.11AC.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_channel_802dot11ac(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=1&start=-3600s&type=radio_channel'

        """
        return self.__radio_graph(u'radio_channel', u'ac', start, end)

    def radio_noise_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for radio noise for radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_noise_802dot11bgn(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=1&radio_interface=2&start=-3600s&type=radio_noise'

        """
        return self.__radio_graph(u'radio_noise', u'bgn', start, end)

    def radio_noise_802dot11an(self, start=None, end=None):
        """RRD graph URL for radio noise for radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_noise_802dot11an(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=1&start=-3600s&type=radio_noise'

        """
        return self.__radio_graph(u'radio_noise', u'aN', start, end)

    def radio_noise_802dot11ac(self, start=None, end=None):
        """RRD graph URL for radio noise for radio type IEEE802.11AC.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_noise_802dot11ac(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=1&start=-3600s&type=radio_noise'

        """
        return self.__radio_graph(u'radio_noise', u'ac', start, end)

    def radio_power_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for radio power for radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_power_802dot11bgn(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=1&radio_interface=2&start=-3600s&type=radio_power'

        """
        return self.__radio_graph(u'radio_power', u'bgn', start, end)

    def radio_power_802dot11an(self, start=None, end=None):
        """RRD graph URL for radio power for radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_power_802dot11an(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=2&start=-3600s&type=radio_power'

        """
        return self.__radio_graph(u'radio_power', u'aN', start, end)

    def radio_power_802dot11ac(self, start=None, end=None):
        """RRD graph URL for radio power for radio type IEEE802.11AC.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_power_802dot11ac(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=2&start=-3600s&type=radio_power'

        """
        return self.__radio_graph(u'radio_power', u'ac', start, end)

    def radio_errors_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for radio errors for radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_errors_802dot11bgn(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=1&radio_interface=2&start=-3600s&type=radio_errors'

        """
        return self.__radio_graph(u'radio_errors', u'bgn', start, end)

    def radio_errors_802dot11an(self, start=None, end=None):
        """RRD graph URL for radio errors for radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_errors_802dot11an(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=2&start=-3600s&type=radio_errors'

        """
        return self.__radio_graph(u'radio_errors', u'aN', start, end)

    def radio_errors_802dot11ac(self, start=None, end=None):
        """RRD graph URL for radio errors for radio type IEEE802.11AC.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_errors_802dot11ac(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=2&start=-3600s&type=radio_errors'

        """
        return self.__radio_graph(u'radio_errors', u'ac', start, end)

    def radio_goodput_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for radio goodput for radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_goodput_802dot11bgn(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=1&radio_interface=2&start=-3600s&type=radio_goodput'

        """
        return self.__radio_graph(u'radio_goodput', u'bgn', start, end)

    def radio_goodput_802dot11an(self, start=None, end=None):
        """RRD graph URL for radio goodput for radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_goodput_802dot11an(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=2&start=-3600s&type=radio_goodput'

        """
        return self.__radio_graph(u'radio_goodput', u'aN', start, end)

    def radio_goodput_802dot11ac(self, start=None, end=None):
        """RRD graph URL for radio goodput for radio type IEEE802.11AC.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.radio_goodput_802dot11ac(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=2&start=-3600s&type=radio_goodput'

        """
        return self.__radio_graph(u'radio_goodput', u'ac', start, end)

    def channel_utilization_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for channel utilization for radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.channel_utilization_802dot11bgn(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=1&radio_interface=2&start=-3600s&type=channel_utilization'

        """
        return self.__radio_graph(u'channel_utilization', u'bgn', start, end)

    def channel_utilization_802dot11an(self, start=None, end=None):
        """RRD graph URL for channel utilization for radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.channel_utilization_802dot11an(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=2&start=-3600s&type=channel_utilization'

        """
        return self.__radio_graph(u'channel_utilization', u'aN', start, end)

    def channel_utilization_802dot11ac(self, start=None, end=None):
        """RRD graph URL for channel utilization for radio type IEEE802.11AC.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is -7200.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> ap_graph.channel_utilization_802dot11ac(start=-3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=00%3A00%3A10%3A00%3A00%3A03&
                end=-0s&radio_index=2&radio_interface=2&start=-3600s&type=channel_utilization'

        """
        return self.__radio_graph(u'channel_utilization', u'ac', start, end)

    @staticmethod
    def urlencode(params):
        """URL Encode."""
        params = sorted(params.items())
        return requests.packages.urllib3.request.urlencode(params)

    @staticmethod
    def graph_time_format(seconds):
        """Graph time format."""
        pat = re.compile(r'(-?\d+)')
        res = pat.search(str(seconds))
        num = 0
        if res:
            num = res.group(0)
        return '{0}s'.format(num)

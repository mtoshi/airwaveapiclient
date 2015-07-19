# -*- coding: utf-8 -*-

"""airwaveapiclient.ap_graph"""


import requests
from requests.compat import urljoin
from collections import OrderedDict


class APGraph(OrderedDict):

    """Aruba networks AirWave Graph.

    Attributes:

        :url (str): AirWave URL.
        :path (str): Graph path.

    """

    def __init__(self, url, obj):
        """Initialize AirWaveAPIClient.

        Args:

            :ap_node (str): AP.

        Usage: ::

            >>> from airwaveapiclient import APGraph
            >>>

        """
        self.url = url
        self.path = '/nf/rrd_graph'
        self.default_start_time = -7200
        OrderedDict.__init__(self, obj)

    @staticmethod
    def urlencode(params):
        """URL Encode."""
        params = sorted(params.items())
        return requests.packages.urllib3.request.urlencode(params)

    def __graph_url(self, params):
        """RRD Graph URL."""
        start = params['start']
        if not start:
            start = self.default_start_time

        end = params['end']
        if not end:
            end = 0

        params['start'] = '%ss' % start
        params['end'] = '%ss' % end
        params = APGraph.urlencode(params)
        path = urljoin(self.url, self.path)
        return '%s?%s' % (path, params)

    def __ap_graph(self, graph_type, radio_type, start, end):
        """RRD access point graph base method.

        Args:

            :graph_type (str): Graph type.
            :radio_type (str): Radio type.
            :start (int, optional): Graph start time(seconds ago).
                Default is None.
            :end (int, optional): Graph end time(seconds ago).
                Default is None.

        Returns:

            :str: Graph URL string.

        """
        params = {}
        params['type'] = graph_type
        params['id'] = self['@id']
        if 'radio' in self:
            for radio in self['radio']:
                if 'radio_type' in radio:
                    if radio['radio_type'] == radio_type:
                        params['radio_index'] = radio['@index']
                        params['start'] = start
                        params['end'] = end
        return self.__graph_url(params)

    def client_count_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for access point client count for radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is None.
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
        """RRD graph URL for access point client count for radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is None.
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

    def bandwidth_802dot11bgn(self, start=None, end=None):
        """RRD graph URL for access point bandwidth for radio type IEEE802.11BGN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is None.
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
        """RRD graph URL for access point bandwidth for radio type IEEE802.11AN.

        Args:

            :start (int, optional): Graph start time(seconds ago).
                Default is None.
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

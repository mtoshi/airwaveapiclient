# -*- coding: utf-8 -*-

"""airwaveapiclient."""


import xmltodict
import requests
import json


class AirWaveAPIClient(object):

    """Aruba networks Air Wave API client.


    """

    def __init__(self, start_times=None, **kwargs):
        """Constructor."""
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.address = kwargs['address']
        self.session = None
        self.start_times = AirWaveAPIClient.set_graph_start_times(start_times)

    def login(self):
        """Login."""
        requests.packages.urllib3.disable_warnings()
        self.session = requests.Session()
        url = 'https://%s/LOGIN' % self.address
        destination = '/'
        params = {'credential_0': self.username,
                  'credential_1': self.password,
                  'login': 'Log In',
                  'destination': destination}
        res = self.session.get(url, params=params, verify=False)
        return {
            'status_code': res.status_code,
            'cookies': self.session.cookies.get_dict()
        }

    def logout(self):
        """Logout."""
        self.session.close()

    def api_path(self, path):
        """API URL."""
        return 'https://%s/%s' % (self.address, path)

    def ap_list(self, ap_ids=None):
        """Get Access Point list."""
        url = self.api_path('ap_list.xml')
        if ap_ids:
            params = AirWaveAPIClient.id_params(ap_ids)
            return self.session.get(url, verify=False, params=params)
        return self.session.get(url, verify=False)

    def ap_nodes(self, ap_ids=None):
        """Get Access Point node list."""
        res = self.ap_list(ap_ids)
        if res.status_code == 200:
            obj = AirWaveAPIClient.xml_to_dict(res.text)
            return obj['amp:amp_ap_list']['ap']
        return []

    def ap_detail(self, ap_id):
        """Get Access Point detail inforamtion."""
        url = self.api_path('ap_detail.xml')
        params = {'id': ap_id}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def client_detail(self, mac):
        """Client detail inforamtion."""
        url = self.api_path('client_detail.xml')
        params = {'mac': mac}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def rogue_detail(self, ap_id):
        """Rogue detail inforamtion."""
        url = self.api_path('rogue_detail.xml')
        params = {'id': ap_id}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def report_list(self, reports_search_title=None):
        """Report list inforamtion."""
        url = self.api_path('/nf/reports_list')
        params = {'format': 'xml'}
        if reports_search_title:
            params['reports_search_title'] = reports_search_title
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def report_detail(self, report_id):
        """Report detail inforamtion."""
        url = self.api_path('/nf/report_detail')
        params = {'id': report_id, 'format': 'xml'}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def graph_url(self, params):
        """RRD Graph URL. """
        url = self.api_path('/nf/rrd_graph')
        params['start'] = '-%ss' % params['start']
        params['end'] = '-%ss' % params['end']
        params = AirWaveAPIClient.urlencode(params)
        return '%s?%s' % (url, params)

    def graph_url_ap_base(self, graph_type, **kwargs):
        """RRD Graph URL for Access Point Base.

        Args :

            :graph_type (str): Graph Type.

        Keyword Args :

            :ap_id (int): Access Point ID.
            :radio_index (int): Access Point Radio type index.
            :start (int): Graph start time.
                 Seconds of current time difference.
                 1 hour ago is 3600.
                 2 hours ago is 7200.
                 3 days ago is 259200(3600sec x 24H x 3days).
            :end (int, optional): Graph end time.
                 Seconds of current time difference.
                 Default is 0.

        Returns:

            :str: Graph URL string.

        """

        params = {'id': kwargs['ap_id'],
                  'radio_index': kwargs['radio_index'],
                  'start': kwargs['start'],
                  'end': kwargs.get('end', 0),
                  'type': graph_type}
        return self.graph_url(params)

    def graph_url_ap_client_count(self, **kwargs):
        """RRD Graph URL for Access Point Client Count."""
        return self.graph_url_ap_base('ap_client_count', **kwargs)

    def graph_url_ap_bandwidth(self, **kwargs):
        """RRD Graph URL for Access Point Bandwidth."""
        return self.graph_url_ap_base('ap_bandwidth', **kwargs)

    def graph_url_dot11_counters(self, **kwargs):
        """RRD Graph URL for 802.11 Counters."""
        return self.graph_url_ap_base('dot11_counters', **kwargs)

    def graph_url_radio_base(self, graph_type, **kwargs):
        """RRD Graph URL for Radio Base.

        Args :

            :graph_type (str): Graph Type.

        Keyword Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
            :graph_type (str): Graph type name.
            :start (int): Graph start time.
                 Seconds of current time difference.
                 1 hour ago is 3600.
                 2 hours ago is 7200.
                 3 days ago is 259200(3600sec x 24H x 3days).
            :end (int, optional): Graph end time.
                 Seconds of current time difference.
                 Default is 0.

        Returns:

            :str: Graph URL string.

        """

        params = {'ap_uid': kwargs['ap_uid'],
                  'radio_index': kwargs['radio_index'],
                  'radio_interface': kwargs['radio_interface'],
                  'start': kwargs['start'],
                  'end': kwargs.get('end', 0),
                  'type': graph_type}
        return self.graph_url(params)

    def graph_url_radio_channel(self, **kwargs):
        """RRD Graph URL for Radio Channel."""
        return self.graph_url_radio_base('radio_channel', **kwargs)

    def graph_url_radio_noise(self, **kwargs):
        """RRD Graph URL for Radio Noise."""
        return self.graph_url_radio_base('radio_noise', **kwargs)

    def graph_url_radio_power(self, **kwargs):
        """RRD Graph URL for Radio Power."""
        return self.graph_url_radio_base('radio_power', **kwargs)

    def graph_url_radio_errors(self, **kwargs):
        """RRD Graph URL for Radio Errors."""
        return self.graph_url_radio_base('radio_errors', **kwargs)

    def graph_url_radio_goodput(self, **kwargs):
        """RRD Graph URL for Radio GoodPut."""
        return self.graph_url_radio_base('radio_goodput', **kwargs)

    def graph_url_channel_utilization(self, **kwargs):
        """RRD Graph URL for Channel utilization."""
        return self.graph_url_radio_base('channel_utilization', **kwargs)

    # pylint: disable=too-many-statements
    def ap_graphs(self, ap_node):
        """Access Point Graph list."""
        graphs = {}

        if 'radio' in ap_node:
            for radio in ap_node['radio']:

                # AP CLIENT COUNT
                key = 'ap_client_count'
                graphs[key] = []
                for start in self.start_times:
                    url = self.graph_url_ap_client_count(
                        ap_id=ap_node['@id'],
                        radio_index=radio['@index'],
                        start=start,
                    )
                    label = AirWaveAPIClient.time_label(start)
                    label = 'AP Client Count %s.' % label
                    graphs[key].append({'label': label, 'url': url})

                # AP BANDWIDTH
                key = 'ap_bandwidth'
                graphs[key] = []
                for start in self.start_times:
                    url = self.graph_url_ap_bandwidth(
                        ap_id=ap_node['@id'],
                        radio_index=radio['@index'],
                        start=start,
                    )
                    label = AirWaveAPIClient.time_label(start)
                    label = 'AP Bandwidth %s.' % label
                    graphs[key].append({'label': label, 'url': url})

                # DOT11 COUNTERS
                key = 'dot11_counters'
                graphs[key] = []
                for start in self.start_times:
                    url = self.graph_url_dot11_counters(
                        ap_id=ap_node['@id'],
                        radio_index=radio['@index'],
                        start=start,
                    )
                    label = AirWaveAPIClient.time_label(start)
                    label = '802.11 Counters %s.' % label
                    graphs[key].append({'label': label, 'url': url})

                # RADIO CHANNEL
                key = 'radio_channel'
                graphs[key] = []
                for start in self.start_times:
                    url = self.graph_url_radio_channel(
                        ap_uid=ap_node['lan_mac'],
                        radio_index=radio['@index'],
                        radio_interface=radio['radio_interface'],
                        start=start,
                    )
                    label = AirWaveAPIClient.time_label(start)
                    label = 'Radio Channel %s.' % label
                    graphs[key].append({'label': label, 'url': url})

                # RADIO NOISE
                key = 'radio_noise'
                graphs[key] = []
                for start in self.start_times:
                    url = self.graph_url_radio_noise(
                        ap_uid=ap_node['lan_mac'],
                        radio_index=radio['@index'],
                        radio_interface=radio['radio_interface'],
                        start=start,
                    )
                    label = AirWaveAPIClient.time_label(start)
                    label = 'Radio Noise %s.' % label
                    graphs[key].append({'label': label, 'url': url})

                # RADIO ERRORS
                key = 'radio_erros'
                graphs[key] = []
                for start in self.start_times:
                    url = self.graph_url_radio_errors(
                        ap_uid=ap_node['lan_mac'],
                        radio_index=radio['@index'],
                        radio_interface=radio['radio_interface'],
                        start=start,
                    )
                    label = AirWaveAPIClient.time_label(start)
                    label = 'Radio Errors %s.' % label
                    graphs[key].append({'label': label, 'url': url})

                # RADIO POWER
                key = 'radio_power'
                graphs[key] = []
                for start in self.start_times:
                    url = self.graph_url_radio_power(
                        ap_uid=ap_node['lan_mac'],
                        radio_index=radio['@index'],
                        radio_interface=radio['radio_interface'],
                        start=start,
                    )
                    label = AirWaveAPIClient.time_label(start)
                    label = 'Radio Power %s.' % label
                    graphs[key].append({'label': label, 'url': url})

                # RADIO GOODPUT
                key = 'radio_goodput'
                graphs[key] = []
                for start in self.start_times:
                    url = self.graph_url_radio_goodput(
                        ap_uid=ap_node['lan_mac'],
                        radio_index=radio['@index'],
                        radio_interface=radio['radio_interface'],
                        start=start,
                    )
                    label = AirWaveAPIClient.time_label(start)
                    label = 'Radio Good Put %s.' % label
                    graphs[key].append({'label': label, 'url': url})

                # CHANNEL CUTILIZATION
                key = 'channel_utilization'
                graphs[key] = []
                for start in self.start_times:
                    url = self.graph_url_channel_utilization(
                        ap_uid=ap_node['lan_mac'],
                        radio_index=radio['@index'],
                        radio_interface=radio['radio_interface'],
                        start=start,
                    )
                    label = AirWaveAPIClient.time_label(start)
                    label = 'Channel Utilization %s.' % label
                    graphs[key].append({'label': label, 'url': url})

        return graphs

    @staticmethod
    def set_graph_start_times(start_times):
        """Default graph start time."""
        if start_times:
            return start_times
        return (3600,
                3600*2,
                3600*3,
                3600*12,
                3600*24,
                3600*24*2,
                3600*24*3,
                3600*24*7,
                3600*24*30,
                3600*24*90,
                3600*24*180,
                3600*24*360)

    @staticmethod
    def id_params(ap_ids):
        """Make access point id string."""
        return '&'.join(["id=%s" % ap_id for ap_id in ap_ids])

    @staticmethod
    def url_params(params):
        """Make url params string."""
        return '&'.join(['%s=%s' % (key, val) for key, val in params.items()])

    @staticmethod
    def xml_to_dict(xml):
        """Change XML to dict."""
        return xmltodict.parse(xml)

    @staticmethod
    def dict_to_json(dict_obj):
        """Change dict to json."""
        return json.dumps(dict_obj)

    @staticmethod
    def urlencode(params):
        """URL Encode."""
        return requests.packages.urllib3.request.urlencode(params)

    @staticmethod
    def time_label(sec):
        """Time labeling for graph time."""
        if sec > 0:
            day = 3600*24
            hour = 3600
            minute = 60
            if sec >= day:
                val = sec / day
                return '%d day(s)' % val
            elif sec >= hour:
                val = sec / hour
                return '%d hour(s)' % val
            elif sec >= minute:
                val = sec / minute
                return '%d minute(s)' % val
        return '%d second(s)' % sec

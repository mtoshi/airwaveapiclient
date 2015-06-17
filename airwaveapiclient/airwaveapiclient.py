# -*- coding: utf-8 -*-

"""airwaveapiclient."""


import xmltodict
import requests
import json


class AirWaveAPIClient(object):

    """Aruba networks Air Wave API client.


    """

    def __init__(self, **kwargs):
        """Constructor."""
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.address = kwargs['address']
        self.session = None

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

    def ap_detail(self, ap_id):
        """Get Access Point detail inforamtion."""
        url = self.api_path('ap_detail.xml')
        params = {'id': ap_id}
        return self.session.get(url, verify=False, params=params)

    def client_detail(self, mac):
        """Client detail inforamtion."""
        url = self.api_path('client_detail.xml')
        params = {'mac': mac}
        return self.session.get(url, verify=False, params=params)

    def rogue_detail(self, ap_id):
        """Rogue detail inforamtion."""
        url = self.api_path('rogue_detail.xml')
        params = {'id': ap_id}
        return self.session.get(url, verify=False, params=params)

    def report_detail(self, report_id):
        """Report detail inforamtion."""
        url = self.api_path('/nf/report_detail')
        params = {'id': report_id, 'format': 'xml'}
        return self.session.get(url, verify=False, params=params)

    def graph_url(self, params):
        """RRD Graph URL. """
        url = self.api_path('/nf/rrd_graph')
        params['start'] = '-%ss' % params['start']
        params['end'] = '-%ss' % params['end']
        params = AirWaveAPIClient.url_params(params)
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

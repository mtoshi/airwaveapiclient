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

    def graph_url_ap_client_count(self, ap_id, radio_index, start, end=0):
        """RRD Graph URL for API Client Count.

        Args :

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

        params = {'id': ap_id,
                  'radio_index': radio_index,
                  'start': start,
                  'end': end,
                  'type': 'ap_client_count'}
        return self.graph_url(params)

    def graph_url_ap_bandwidth(self, ap_id, radio_index, start, end=0):
        """RRD Graph URL for Access Point Bandwidth.

        Args :

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

        params = {'id': ap_id,
                  'radio_index': radio_index,
                  'start': start,
                  'end': end,
                  'type': 'ap_bandwidth'}
        return self.graph_url(params)

    def graph_url_radio_channel(self, ap_uid, radio_index, radio_interface,
                                start, end=0):
        """RRD Graph URL for Radio Channel.

        Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
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

        params = {'ap_uid': ap_uid,
                  'radio_index': radio_index,
                  'radio_interface': radio_interface,
                  'start': start,
                  'end': end,
                  'type': 'radio_channel'}
        return self.graph_url(params)

    def graph_url_radio_noise(self, ap_uid, radio_index, radio_interface,
                              start, end=0):
        """RRD Graph URL for Radio Noise.

        Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
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

        params = {'ap_uid': ap_uid,
                  'radio_index': radio_index,
                  'radio_interface': radio_interface,
                  'start': start,
                  'end': end,
                  'type': 'radio_noise'}
        return self.graph_url(params)

    def graph_url_radio_power(self, ap_uid, radio_index, radio_interface,
                              start, end=0):
        """RRD Graph URL for Radio Noise.

        Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
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

        params = {'ap_uid': ap_uid,
                  'radio_index': radio_index,
                  'radio_interface': radio_interface,
                  'start': start,
                  'end': end,
                  'type': 'radio_power'}
        return self.graph_url(params)

    def graph_url_radio_errors(self, ap_uid, radio_index, radio_interface,
                               start, end=0):
        """RRD Graph URL for Radio Errors.

        Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
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

        params = {'ap_uid': ap_uid,
                  'radio_index': radio_index,
                  'radio_interface': radio_interface,
                  'start': start,
                  'end': end,
                  'type': 'radio_errors'}
        return self.graph_url(params)

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

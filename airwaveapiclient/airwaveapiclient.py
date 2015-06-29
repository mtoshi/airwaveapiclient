# -*- coding: utf-8 -*-

"""airwaveapiclient."""


import requests
import os
import xmltodict
from collections import OrderedDict


class AirWaveAPIClient(object):

    """class AirWaveAPIClient.

    Aruba networks AirWave API client.

    Attributes:

        username (str): Login username.
        password (str): Login password.
        address (str): Host name or ip address.
        session (requests.sessions.Session): Session for connection pooling.

    """

    def __init__(self, **kwargs):
        """Constructor.

        Args:

            username (str): Login username.
            password (str): Login password.
            address (str): Host name or ip address.

        Usage ::

            >>> from airwaveapiclient import AirWaveAPIClient
            >>> airwave = AirWaveAPIClient(username='admin',
            >>>                            password='xxxxx',
            >>>                            address='192.168.1.1')
            >>>


        """
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.address = kwargs['address']
        self.session = None

    def login(self):
        """Login.

        Returns:

            requests.models.Response

        Usage ::

            >>> res = obj.login()
            >>> res.status_code
            200


        """
        requests.packages.urllib3.disable_warnings()
        self.session = requests.Session()
        url = 'https://%s/LOGIN' % self.address
        destination = '/'
        next_action = ''
        params = {'credential_0': self.username,
                  'credential_1': self.password,
                  'login': 'Log In',
                  'destination': destination,
                  'next_action': next_action}
        return self.session.post(url, params=params, verify=False)

    def logout(self):
        """Logout.

        Close the session.

        """
        self.session.close()

    def api_path(self, path):
        """API URL.

        Args:

            path (str): Path for API URL.

        Returns:

            URL string 'https://xxx.xxx.xxx.xxx/xxxxxx'

        """
        url = 'https://%s/' % self.address
        return os.path.join(url, path)

    def ap_list(self, ap_ids=None):
        """Get Access Point list.

        Memo:

            This API output is XML.

        Args:

            ap_ids (optional[list]): You may specify multiple Access Point IDs.
                Default is None.

        Returns:

            requests.models.Response

        Usage ::

            Get all Acces Point.

            >>> res = obj.ap_list()
            >>> res.url
            'https://192.168.1.1/ap_list.xml'

            Get specified Acces Point.

            >>> res = obj.ap_list([123, 124, 125])
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/ap_list.xml?id=123&id=124&id=125'
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'


        """
        url = self.api_path('ap_list.xml')
        if ap_ids:
            params = AirWaveAPIClient.id_params(ap_ids)
            return self.session.get(url, verify=False, params=params)
        return self.session.get(url, verify=False)

    def ap_detail(self, ap_id):
        """Get Access Point detail inforamtion.

        Memo:

            This API output is XML.

        Args:

            ap_id (int): Access Point ID.

        Returns:

            requests.models.Response

        Usage ::

            >>> res = obj.ap_detail(123)
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/ap_detail.xml?id=123'
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'


        """
        url = self.api_path('ap_detail.xml')
        params = {'id': ap_id}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def client_detail(self, mac):
        """Client detail inforamtion.

        Memo:

            This API output is XML.

        Args:

            mac (str): Client device's MAC address.

        Returns:

            requests.models.Response

        Usage ::

            >>> res = obj.client_detail('12:34:56:78:90:AB')
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/client_detail.xml?mac=12%3A34%3A56%3A78%3A90%3AAB'
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'


        """
        url = self.api_path('client_detail.xml')
        params = {'mac': mac}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def rogue_detail(self, ap_id):
        """Rogue detail inforamtion.

        Memo:

            This API output is XML.

        Args:

            ap_id (int): Access Point ID.

        Returns:

            requests.models.Response

        Usage ::

            >>> res = obj.rogue_detail(123)
            >>> res.status_code
            200
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'


        """
        url = self.api_path('rogue_detail.xml')
        params = {'id': ap_id}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def report_list(self, reports_search_title=None):
        """Report list inforamtion.

        Memo:

            This API output is XHTML(not XML).

        Args:

            reports_search_title (optional[str]): You may filter with
                report title.  Default is None.

        Returns:

            requests.models.Response

        Usage ::

            Get report list.

            >>> res = obj.report_list()
            >>> res.url
            'https://192.168.1.1/nf/reports_list?format=xml'

            Get specified report list with title.

            >>> res = obj.report_list('Weekly Report')
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/nf/reports_list?reports_search_title=Weekly+Report&format=xml'
            >>> res.text  # xhtml output.
            '<?xml version="1.0"?><!DOCTYPE html ...'


        """
        url = self.api_path('nf/reports_list')
        params = {'format': 'xml'}
        if reports_search_title:
            params['reports_search_title'] = reports_search_title
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def report_detail(self, report_id):
        """Report detail inforamtion.

        Memo:

            This API output is XHTML(not XML).

        Args:

            report_id (int): Report ID.

        Returns:

            requests.models.Response

        Usage ::

            >>> res = obj.report_detail(123)
            >>> res.status_code
            200
            >>> res.url
            'https://192.1681.1/nf/report_detail?id=123&format=xml'
            >>> res.text  # xhtml output.
            '<?xml version="1.0"?><!DOCTYPE html ...'


        """
        url = self.api_path('nf/report_detail')
        params = {'id': report_id, 'format': 'xml'}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def __graph_url(self, params):
        """RRD Graph URL."""
        url = self.api_path('nf/rrd_graph')
        params['start'] = '-%ss' % params['start']
        params['end'] = '-%ss' % params['end']
        params = AirWaveAPIClient.urlencode(params)
        return '%s?%s' % (url, params)

    def ap_base_url(self, graph_type, **kwargs):
        """RRD Graph Base URL for Access Point.

        Args :

            graph_type (str): Graph Type.

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
        return self.__graph_url(params)

    def ap_client_count_graph_url(self, **kwargs):
        """RRD Graph URL for Access Point Client Count.

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

        Usage ::

            >>> airwave.ap_client_count_graph_url(ap_id=1,
            ...                                   radio_index=1,
            ...                                   start=3600)


        """
        return self.ap_base_url('ap_client_count', **kwargs)

    def ap_bandwidth_graph_url(self, **kwargs):
        """RRD Graph URL for Access Point Bandwidth.

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

            str: Graph URL string.

        Usage ::

            >>> airwave.ap_bandwidth_graph_url(ap_id=1,
            ...                                radio_index=1,
            ...                                start=3600)


        """
        return self.ap_base_url('ap_bandwidth', **kwargs)

    def dot11_counters_graph_url(self, **kwargs):
        """RRD Graph URL for 802.11 Counters.

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

        Usage ::

            >>> airwave.dot11_counters_graph_url(ap_id=1,
            ...                                  radio_index=1,
            ...                                  start=3600)


        """

        return self.ap_base_url('dot11_counters', **kwargs)

    def radio_base_url(self, graph_type, **kwargs):
        """RRD Graph URL for Radio Base.

        Args :

            graph_type (str): Graph Type.

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
        return self.__graph_url(params)

    def radio_channel_graph_url(self, **kwargs):
        """RRD Graph URL for Radio Channel.

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

        Usage ::

            >>> airwave.radio_channel_graph_url(ap_uid="01:23:45:67:89:AB",
            ...                                 radio_index=1,
            ...                                 radio_interface=1,
            ...                                 start=3600)


        """

        return self.radio_base_url('radio_channel', **kwargs)

    def radio_noise_graph_url(self, **kwargs):
        """RRD Graph URL for Radio Noise.

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

        Usage ::

            >>> airwave.radio_noise_graph_url(ap_uid="01:23:45:67:89:AB",
            ...                               radio_index=1,
            ...                               radio_interface=1,
            ...                               start=3600)


        """

        return self.radio_base_url('radio_noise', **kwargs)

    def radio_power_graph_url(self, **kwargs):
        """RRD Graph URL for Radio Power.

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

        Usage ::

            >>> airwave.radio_power_graph_url(ap_uid="01:23:45:67:89:AB",
            ...                               radio_index=1,
            ...                               radio_interface=1,
            ...                               start=3600)


        """

        return self.radio_base_url('radio_power', **kwargs)

    def radio_errors_graph_url(self, **kwargs):
        """RRD Graph URL for Radio Errors.

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

        Usage ::

            >>> airwave.radio_errors_graph_url(ap_uid="01:23:45:67:89:AB",
            ...                                radio_index=1,
            ...                                radio_interface=1,
            ...                                start=3600)


        """

        return self.radio_base_url('radio_errors', **kwargs)

    def radio_goodput_graph_url(self, **kwargs):
        """RRD Graph URL for Radio GoodPut.

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

        Usage ::

            >>> airwave.radio_goodput_graph_url(ap_uid="01:23:45:67:89:AB",
            ...                                 radio_index=1,
            ...                                 radio_interface=1,
            ...                                 start=3600)


        """

        return self.radio_base_url('radio_goodput', **kwargs)

    def channel_utilization_graph_url(self, **kwargs):
        """RRD Graph URL for Channel utilization.

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

        Usage ::

            >>> airwave.channel_utilization_graph_url(
            ...     ap_uid="01:23:45:67:89:AB",
            ...     radio_index=1,
            ...     radio_interface=1,
            ...     start=3600)


        """

        return self.radio_base_url('channel_utilization', **kwargs)

    @staticmethod
    def id_params(ap_ids):
        """Make access point id string."""
        return '&'.join(["id=%s" % ap_id for ap_id in ap_ids])

    @staticmethod
    def urlencode(params):
        """URL Encode."""
        params = sorted(params.items())
        return requests.packages.urllib3.request.urlencode(params)


class APList(object):

    """class APList.

    Access Point List.

    Attributes:

        xml (str): API XML string.


    """

    def __init__(self, xml):
        """Constructor."""
        self.xml = xml

    def nodes(self):
        """Access Point Nodes.

        Returns:

            list: Access Point node list.

        """
        data = xmltodict.parse(self.xml)
        ap_nodes = data['amp:amp_ap_list']['ap']
        return [APNode(ap_node) for ap_node in ap_nodes]


class APNode(OrderedDict):

    """class APNode.

    Access Point Node.

    Attributes:

        xml (str): API XML string.


    """

    def __init__(self, *args):
        """Constructor."""
        OrderedDict.__init__(self, *args)

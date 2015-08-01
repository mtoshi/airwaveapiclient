# -*- coding: utf-8 -*-

"""airwaveapiclient."""


import requests
import os
import xmltodict
from collections import OrderedDict


class AirWaveAPIClient(object):

    """Aruba networks AirWave API client.

    Attributes:

        :username (str): AirWave Login username.
        :password (str): AirWave Login password.
        :url (str): AirWave URL.
        :session (requests.sessions.Session): Session for connection pooling.

    """

    def __init__(self, **kwargs):
        """Initialize AirWaveAPIClient.

        Args:

            :username (str): AirWave Login username.
            :password (str): AirWave Login password.
            :url (str): AirWave url.

        Usage: ::

            >>> from airwaveapiclient import AirWaveAPIClient
            >>> airwave = AirWaveAPIClient(username='admin',
            >>>                            password='xxxxx',
            >>>                            url='https://192.168.1.1/')
            >>>


        """
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.url = kwargs['url']
        self.session = None

    def login(self):
        """Login to AirWave.

        Returns:

            requests.models.Response

        Usage: ::

            >>> res = airwave.login()
            >>> res.status_code
            200

        """
        requests.packages.urllib3.disable_warnings()
        self.session = requests.Session()
        url = os.path.join(self.url, 'LOGIN')
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

        Usage: ::

            >>> airwave.logout()

        """
        self.session.close()

    def api_path(self, path):
        """API URL.

        Args:

            :path (str): Path for API URL.

        Returns:

            URL string 'https://xxx.xxx.xxx.xxx/xxxxxx'

        """
        return os.path.join(self.url, path)

    def ap_list(self, ap_ids=None):
        """Get Access Point list.

        Args:

            :ap_ids (optional[list]): You may specify multiple
                Access Point IDs. Default is None.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            # Get all Acces Point.

            >>> res = airwave.ap_list()
            >>> res.url
            'https://192.168.1.1/ap_list.xml'

            # Get specified Acces Point.

            >>> res = airwave.ap_list([123, 124, 125])
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

        Args:

            :ap_id (int): Access Point ID.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.ap_detail(123)
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

        Args:

            :mac (str): Client device's MAC address.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.client_detail('12:34:56:78:90:AB')
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

        Args:

            :ap_id (int): Access Point ID.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.rogue_detail(123)
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

        .. warning::

            This method result includes API output that is XHTML(not XML).

        Args:

            :reports_search_title (optional[str]): You may filter with
                report title.  Default is None.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            # Get report list.

            >>> res = airwave.report_list()
            >>> res.url
            'https://192.168.1.1/nf/reports_list?format=xml'

            # Get specified report list with title.

            >>> res = airwave.report_list('Weekly Report')
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

        .. warning::

            This method result includes API output that is XHTML(not XML).

        Args:

            :report_id (int): Report ID.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.report_detail(123)
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

    @staticmethod
    def id_params(ap_ids):
        """Make access point id string."""
        return '&'.join(["id=%s" % ap_id for ap_id in ap_ids])

    @staticmethod
    def urlencode(params):
        """URL Encode."""
        params = sorted(params.items())
        return requests.packages.urllib3.request.urlencode(params)


class APList(list):

    """Access Point List.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize APList.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import AirWaveAPIClient
            >>> from airwaveapiclient import APList
            >>> airwave = AirWaveAPIClient(username='admin',
            >>>                            password='xxxxx',
            >>>                            url='https://192.168.1.1/')
            >>> airwave.login()
            >>> res = airwave.ap_list()
            >>> airwave.logout()
            >>> objs = APList(res.text)
            >>> for obj apin objs:
            ...     'ID:%s, %s' % (obj['@id'], obj['name'])
            'ID:1, AP001'
            'ID:2, AP002'
            'ID:3, AP003'

        """
        data = xmltodict.parse(xml)
        obj = data['amp:amp_ap_list']['ap']
        list.__init__(self, obj)

    def search(self, obj):
        """Search Access Point.

        This method can search access point with id or name.
        Search Logic is a complete match.

        Args:

            :obj (str or int): Access point id or name.

        """
        if isinstance(obj, int):
            for node in self:
                if int(node['@id']) == obj:
                    return node

        if isinstance(obj, str):
            for node in self:
                if node['name'] == obj:
                    return node
        return None


class APDetail(OrderedDict):

    """Access Point Detail.

    This class inherits the OrderedDict class.

    """
    def __init__(self, xml):
        """Initialize APDetail.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import AirWaveAPIClient
            >>> from airwaveapiclient import APDetail
            >>> airwave = AirWaveAPIClient(username='admin',
            >>>                            password='xxxxx',
            >>>                            url='https://192.168.1.1/')
            >>> airwave.login()
            >>> res = airwave.ap_detail(123)
            >>> airwave.logout()
            >>> obj = APDetail(res.text)
            >>> for radio in obj['radio']:
            ...     for client in radio['client']:
            ...         'ID:%s, SIGNAL:%s, SNR:%s' % (client['@id'],
            ...                                       client['signal'],
            ...                                       client['snr'])
            'ID:11000001, SIGNAL:-43, SNR:51'
            'ID:11000002, SIGNAL:-50, SNR:44'
            'ID:11000003, SIGNAL:-56, SNR:38'

        """
        data = xmltodict.parse(xml)
        obj = data['amp:amp_ap_detail']['ap']
        OrderedDict.__init__(self, obj)

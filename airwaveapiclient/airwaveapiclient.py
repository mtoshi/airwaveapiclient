# -*- coding: utf-8 -*-

"""airwaveapiclient."""


import os
from collections import OrderedDict
import xmltodict
import requests


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

    def amp_stats(self):
        """Get AMP stats.

        Args:

            None

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            # Get AMP stats.

            >>> res = airwave.amp_stats()
            >>> res.url
            'https://192.168.1.1/amp_stats.xml'

            >>> res.status_code
            200

            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('amp_stats.xml')
        return self.session.get(url, verify=False)

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

    def folder_list(self, folder_ids=None):
        """Get Folders list.

        Args:

            :folder_ids (optional[list]): You may specify multiple
                Folder IDs. Default is None.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            # Get all Folders.

            >>> res = airwave.folder_list()
            >>> res.url
            'https://192.168.1.1/folder_list.xml'

            # Get specified Folder.

            >>> res = airwave.folder_list([123, 124, 125])
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/folder_list.xml?id=123&id=124&id=125'
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('folder_list.xml')
        if folder_ids:
            params = AirWaveAPIClient.id_params(folder_ids)
            return self.session.get(url, verify=False, params=params)
        return self.session.get(url, verify=False)

    def ap_detail(self, ap_id):
        """Get Access Point detail information.

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
        """Client detail information.

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
        """Rogue detail information.

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

    def latest_report(self, report_definition_id):
        """Latest report information.

        Args:

            :report_definition_id (int): Report definition ID.
                Please get it from "https://x.x.x.x/reports_definition".

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.latest_report(123)
            >>> res.status_code
            200
            >>> res.url
            'https://192.1681.1/latest_report.xml?id=123'
            >>> res.text
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('latest_report.xml')
        params = {'id': report_definition_id}
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


class Report(OrderedDict):

    """Report.

    This class inherits the OrderedDict class.

    """
    def __init__(self, xml):
        """Initialize Report.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from pprint import pprint
            >>> from airwaveapiclient import AirWaveAPIClient
            >>> from airwaveapiclient import Report
            >>> airwave = AirWaveAPIClient(username='admin',
            >>>                            password='xxxxx',
            >>>                            url='https://192.168.1.1/')
            >>> airwave.login()
            >>> res = airwave.latest_report(123)
            >>> airwave.logout()
            >>> obj = Report(res.text)
            >>> pprint(obj)
            ...
            'pickled_client_summary': {'@avg_session_duration': '6852.8010011',
                                       '@avg_signal': '-48.2753361755045',
                                       '@avg_signal_quality': '40.26971451664',
                                       ...
                                       '@total_sessions': '91',
                                       '@total_traffic': '10759.4415',
                                       '@total_traffic_in': '7725.6606',
                                       '@total_traffic_out': '3033.7809',
                                       '@unique_aps': '2',
                                       '@unique_users': '19'},
            'pickled_ap_summary': [{'@ap_folder_id': '1',
                                    '@ap_folder_path': 'Top > OfficeA',
                                    '@ap_group_id': '1',
                                    '@ap_group_name': 'OfficeA',
                                    '@ap_id': '100',
                                    '@avg_bw': '110.701',
                                    ...

        """
        data = xmltodict.parse(xml)
        obj = data['amp:report']
        OrderedDict.__init__(self, obj)

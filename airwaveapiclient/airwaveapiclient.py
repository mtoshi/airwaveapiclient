# -*- coding: utf-8 -*-

"""airwaveapiclient."""


import requests


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
        return 'https://%s/%s' % (self.address, path)

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

            Get specified report list with title.

            >>> res = obj.report_list('Weekly Report')
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/nf/reports_list?format=xml'
            >>> res.text  # xhtml output.
            '\n\n<?xml version="1.0"?>\n<!DOCTYPE html ...'


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
            '\n\n<?xml version="1.0"?>\n<!DOCTYPE html ...'


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
        return requests.packages.urllib3.request.urlencode(params)

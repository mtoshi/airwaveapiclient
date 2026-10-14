# -*- coding: utf-8 -*-

"""airwaveapiclient."""


import base64
import json
from collections import OrderedDict
import xmltodict
import requests
from urllib.parse import urljoin, urlencode


class AirWaveAPIClient(object):

    """Aruba networks AirWave API client.

    Attributes:

        :username (str): AirWave Login username.
        :password (str): AirWave Login password.
        :url (str): AirWave URL.
        :session (requests.sessions.Session): Session for connection pooling.
        :verify (bool): SSL verification flag.
        :biscotti (str): X-BISCOTTI token for authenticated session.

    """

    def __init__(self, **kwargs):
        """Initialize AirWaveAPIClient.

        Args:

            :username (str): AirWave Login username.
            :password (str): AirWave Login password.
            :url (str): AirWave url.
            :verify (optional[bool]): SSL certificate verification. Default is False.
            :biscotti (optional[str]): Pre-existing X-BISCOTTI token.

        Usage: ::

            >>> from airwaveapiclient import AirWaveAPIClient
            >>> airwave = AirWaveAPIClient(username='admin',
            >>>                            password='xxxxx',
            >>>                            url='https://192.168.1.1/')
            >>>


        """
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.url = kwargs.get('url')
        self.verify = kwargs.get('verify', False)
        self.biscotti = kwargs.get('biscotti', None)
        self.session = None
        if self.biscotti:
            self.session = requests.Session()
            self.session.headers['X-BISCOTTI'] = self.biscotti

    def is_cred_obfusc(self):
        """Check if AirWave server has credential obfuscation enabled.

        Queries the unauthenticated '/api/is_cred_obfusc.json' endpoint.
        If the endpoint is not supported by older AirWave servers (returns 404,
        connection error, or non-JSON), it safely returns False as a fallback.

        Returns:

            bool: True if credential obfuscation is enabled, False otherwise.

        """
        requests.packages.urllib3.disable_warnings()
        url = self.api_path('/api/is_cred_obfusc.json')
        try:
            sess = self.session if self.session is not None else requests.Session()
            res = sess.get(url, verify=self.verify, timeout=5)
            if res.status_code == 200:
                data = res.json()
                return bool(data.get('is_cred_obfuscation') or data.get('is_cred_obfusc'))
        except Exception:
            pass
        return False

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
        if self.session is None:
            self.session = requests.Session()
        if self.biscotti:
            self.session.headers['X-BISCOTTI'] = self.biscotti

        password = self.password
        if password and self.is_cred_obfusc():
            password = base64.b64encode(password.encode('utf-8')).decode('utf-8')

        url = self.api_path('LOGIN')
        destination = '/'
        next_action = ''
        params = {'credential_0': self.username,
                  'credential_1': password,
                  'login': 'Log In',
                  'destination': destination,
                  'next_action': next_action}
        res = self.session.post(url, data=params, params=params, verify=self.verify)
        biscotti = res.headers.get('X-BISCOTTI') or res.headers.get('x-biscotti')
        if biscotti:
            self.biscotti = biscotti
            self.session.headers['X-BISCOTTI'] = biscotti
        return res

    def logout(self):
        """Logout.

        Close the session.

        Usage: ::

            >>> airwave.logout()

        """
        if self.session:
            self.session.headers.pop('X-BISCOTTI', None)
            self.session.close()
        self.biscotti = None

    def api_path(self, path):
        """API URL.

        Args:

            :path (str): Path for API URL.

        Returns:

            URL string 'https://xxx.xxx.xxx.xxx/xxxxxx'

        """
        return urljoin(self.url, path)

    def amp_stats(self, include_all_stats=False, include_bandwidth=False):
        """Get AMP stats.

        Args:

            :include_all_stats (optional[bool]): Include all stats. Default is False.
            :include_bandwidth (optional[bool]): Include bandwidth. Default is False.

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
        params = {}
        if include_all_stats:
            params['include_all_stats'] = 1
        if include_bandwidth:
            params['include_bandwidth'] = 1
        params = AirWaveAPIClient.urlencode(params) if params else None
        return self.session.get(url, verify=self.verify, params=params)

    def ap_list(self, ap_ids=None, folder_id=None, group_id=None, controller_id=None):
        """Get Access Point list.

        Args:

            :ap_ids (optional[int, str, list]): You may specify multiple
                Access Point IDs. Default is None.
            :folder_id (optional[int, str]): Filter by AP folder ID.
            :group_id (optional[int, str]): Filter by AP group ID.
            :controller_id (optional[int, str]): Filter by controller ID.

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
        params_list = []
        if ap_ids:
            if isinstance(ap_ids, (list, tuple, set)):
                for ap_id in ap_ids:
                    params_list.append('id=%s' % ap_id)
            else:
                params_list.append('id=%s' % ap_ids)
        if folder_id is not None:
            params_list.append('ap_folder_id=%s' % folder_id)
        if group_id is not None:
            params_list.append('ap_group_id=%s' % group_id)
        if controller_id is not None:
            params_list.append('controller_id=%s' % controller_id)

        if params_list:
            params = '&'.join(params_list)
            return self.session.get(url, verify=self.verify, params=params)
        return self.session.get(url, verify=self.verify)

    def folder_list(self, folder_ids=None):
        """Get Folders list.

        Args:

            :folder_ids (optional[int, str, list]): You may specify multiple
                Folder IDs. Default is None.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            # Get all Folders.

            >>> res = airwave.folder_list()
            >>> res.url
            'https://192.168.1.1/folder_list.xml'

            # Get specified Folders by ID.

            >>> res = airwave.folder_list([123, 124, 125])
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/folder_list.xml?id=123&id=124&id=125'
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('folder_list.xml')
        if folder_ids is not None:
            if isinstance(folder_ids, (int, str)):
                folder_ids = [folder_ids]
            params = AirWaveAPIClient.id_params(folder_ids)
            return self.session.get(url, verify=self.verify, params=params)
        return self.session.get(url, verify=self.verify)

    def ap_detail(self, ap_ids=None, folder_id=None, group_id=None, controller_id=None, include_ignored=False):
        """Get Access Point detail information.

        Args:

            :ap_ids (optional[int, str, list, tuple, set]): Single Access Point ID or
                multiple IDs. Default is None.
            :folder_id (optional[int, str]): Filter by AP folder ID.
            :group_id (optional[int, str]): Filter by AP group ID.
            :controller_id (optional[int, str]): Filter by controller ID.
            :include_ignored (optional[bool]): Include ignored neighbor APs. Default False.

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

            # Multiple APs query:

            >>> res = airwave.ap_detail([123, 124, 125])
            >>> res.url
            'https://192.168.1.1/ap_detail.xml?id=123&id=124&id=125'

            # Filter by folder, group, or controller:

            >>> res = airwave.ap_detail(folder_id=10, group_id=2)

        """
        url = self.api_path('ap_detail.xml')
        params_list = []
        if ap_ids is not None:
            if isinstance(ap_ids, (list, tuple, set)):
                for ap_id in ap_ids:
                    params_list.append('id=%s' % ap_id)
            else:
                params_list.append('id=%s' % ap_ids)
        if folder_id is not None:
            params_list.append('ap_folder_id=%s' % folder_id)
        if group_id is not None:
            params_list.append('ap_group_id=%s' % group_id)
        if controller_id is not None:
            params_list.append('controller_id=%s' % controller_id)
        if include_ignored:
            params_list.append('include=ignored')

        if params_list:
            params = '&'.join(params_list)
            return self.session.get(url, verify=self.verify, params=params)
        return self.session.get(url, verify=self.verify)

    def ap_search(self, query=None):
        """Return Access Point search results for the query.

        Args:

            :query (str): Query string (partial/complete MAC address).

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.ap_search("00:0B:85:1B:A6:90")
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/ap_search.xml?query=00:0B:85:1B:A6:90'
            >>> res.text # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('ap_search.xml')
        params = {'query': query}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=self.verify, params=params)

    def client_detail(self, mac, limit=None):
        """Client detail information.

        Args:

            :mac (str): Client device's MAC address.
            :limit (optional[int]): Limit historical associations. Default None.

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
        if limit is not None:
            params['limit'] = limit
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=self.verify, params=params)

    def client_search(self, query=None):
        """Return Client search results for the query.

        Args:

            :query (str): Query string (partial/complete MAC address).

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.client_search("00:0E:35:52:8C:AB")
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/client_search.xml?query=00:0E:35:52:8C:AB'
            >>> res.text # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('client_search.xml')
        params = {'query': query}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=self.verify, params=params)

    def client_location(self, mac):
        """Client location information.

        Args:

            :mac (str): Client device's MAC address.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.client_location('12:34:56:78:90:AB')
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/visualrf/location.xml?mac=12%3A34%3A56%3A78%3A90%3AAB'
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('/visualrf/location.xml')
        params = {'mac': mac}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=self.verify, params=params)

    def rogue_detail(self, ap_id, limit=None):
        """Rogue detail information.

        Args:

            :ap_id (int): Access Point ID.
            :limit (optional[int]): Limit discovery events. Default None.

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
        if limit is not None:
            params['limit'] = limit
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=self.verify, params=params)

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
        return self.session.get(url, verify=self.verify, params=params)

    def alert_list(self):
        """Get AirWave alerts list.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.alert_list()
            >>> res.url
            'https://192.168.1.1/alerts.xml'

        """
        url = self.api_path('alerts.xml')
        return self.session.get(url, verify=self.verify)

    def ap_bssid_list(self, ap_ids=None, folder_id=None, group_id=None, controller_id=None):
        """Get Access Point BSSID list.

        Args:

            :ap_ids (optional[int, str, list]): Access point ID(s).
            :folder_id (optional[int, str]): Filter by AP folder ID.
            :group_id (optional[int, str]): Filter by AP group ID.
            :controller_id (optional[int, str]): Filter by controller ID.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.ap_bssid_list([123, 124])
            >>> res.url
            'https://192.168.1.1/api/ap_bssid_list.xml?id=123&id=124'

        """
        url = self.api_path('api/ap_bssid_list.xml')
        params_list = []
        if ap_ids:
            if isinstance(ap_ids, (list, tuple, set)):
                for ap_id in ap_ids:
                    params_list.append('id=%s' % ap_id)
            else:
                params_list.append('id=%s' % ap_ids)
        if folder_id is not None:
            params_list.append('ap_folder_id=%s' % folder_id)
        if group_id is not None:
            params_list.append('ap_group_id=%s' % group_id)
        if controller_id is not None:
            params_list.append('controller_id=%s' % controller_id)

        if params_list:
            params = '&'.join(params_list)
            return self.session.get(url, verify=self.verify, params=params)
        return self.session.get(url, verify=self.verify)

    def ap_log(self, ap_ids, limit=None):
        """Get most recent log messages for Access Points.

        Args:

            :ap_ids (int, str, list): One or more Access Point IDs.
            :limit (optional[int]): Limit number of log entries (default 20).

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.ap_log([12, 13], limit=10)
            >>> res.url
            'https://192.168.1.1/ap_log.xml?id=12&id=13&limit=10'

        """
        url = self.api_path('ap_log.xml')
        params_list = []
        if isinstance(ap_ids, (list, tuple, set)):
            for ap_id in ap_ids:
                params_list.append('id=%s' % ap_id)
        else:
            params_list.append('id=%s' % ap_ids)
        if limit is not None:
            params_list.append('limit=%s' % limit)
        params = '&'.join(params_list)
        return self.session.get(url, verify=self.verify, params=params)

    def user_info(self):
        """Get user authorization information for currently logged-in user.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.user_info()
            >>> res.url
            'https://192.168.1.1/user_info.xml'

        """
        url = self.api_path('user_info.xml')
        return self.session.get(url, verify=self.verify)

    def topology_list(self, folder_id=None):
        """Get topology list of devices in a folder.

        Args:

            :folder_id (optional[int, str]): Folder ID. If None, loads all folders.

        Returns:

            :Response: requests.models.Response (JSON payload).

        Usage: ::

            >>> res = airwave.topology_list(5)
            >>> res.url
            'https://192.168.1.1/topology/getTopology?folderId=5'

        """
        url = self.api_path('topology/getTopology')
        folder_val = str(folder_id) if folder_id is not None else ''
        params = 'folderId=%s' % folder_val
        return self.session.get(url, verify=self.verify, params=params)

    def vpn_user_search(self, query=None):
        """Search VPN users.

        Args:

            :query (str): Query string for VPN user search.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.vpn_user_search("photocrayon")
            >>> res.url
            'https://192.168.1.1/vpn_user_search.xml?query=photocrayon'

        """
        url = self.api_path('vpn_user_search.xml')
        params = {'query': query}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=self.verify, params=params)

    def delete_device(self, device_id):
        """Delete a device by device ID.

        Args:

            :device_id (int, str): Device ID to delete.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.delete_device(1)

        """
        url = self.api_path('api/delete_device')
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'device_id': int(device_id)})
        return self.session.delete(url, data=data, headers=headers, verify=self.verify)

    def move_to_folder(self, device_id, folder_id):
        """Move a device to a folder.

        Args:

            :device_id (int, str): Device ID.
            :folder_id (int, str): Target Folder ID.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.move_to_folder(1, 2)

        """
        url = self.api_path('api/move_to_folder')
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'device_id': int(device_id), 'folder_id': int(folder_id)})
        return self.session.put(url, data=data, headers=headers, verify=self.verify)

    def move_to_group(self, device_id, group_id=None, group_name=None):
        """Move a device to a group.

        Args:

            :device_id (int, str): Device ID.
            :group_id (optional[int, str]): Target Group ID.
            :group_name (optional[str]): Target Group name.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.move_to_group(10, group_id=1)

        """
        url = self.api_path('api/move_to_group')
        headers = {'Content-Type': 'application/json'}
        payload = {'device_id': int(device_id)}
        if group_id is not None:
            payload['group_id'] = int(group_id)
        if group_name is not None:
            payload['group_name'] = str(group_name)
        data = json.dumps(payload)
        return self.session.put(url, data=data, headers=headers, verify=self.verify)

    def ap_allowlist_upload(self, csv_data, append_allowlist=1):
        """Upload AP allowlist in CSV format.

        Args:

            :csv_data (str): AP allowlist in CSV format.
            :append_allowlist (int): 0: Replace whole list, 1: Update without removing.

        Returns:

            :Response: requests.models.Response.

        """
        url = self.api_path('api/ap_allowlist_upload')
        data = {'csv': csv_data, 'append_allowlist': int(append_allowlist)}
        return self.session.post(url, data=data, verify=self.verify)

    def template_variable_update(self, xml_data):
        """Modify or add template variables.

        Args:

            :xml_data (str): Template variable update XML string.

        Returns:

            :Response: requests.models.Response.

        """
        url = self.api_path('template_variable_api')
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'xml': xml_data}
        return self.session.post(url, data=data, headers=headers, verify=self.verify)

    def add_ssl_certificate(self, cert_data, passphrase):
        """Install SSL certificate.

        Args:

            :cert_data (str): Encoded base64 format of pfx file.
            :passphrase (str): Password for certificate.

        Returns:

            :Response: requests.models.Response.

        """
        url = self.api_path('api/add_ssl_certificate')
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'cert_data': cert_data, 'passphrase': passphrase})
        return self.session.post(url, data=data, headers=headers, verify=self.verify)

    def visualrf_campus(self, campus_id=None, buildings=None, sites=None, aps=None, messages=None):
        """Query VisualRF campus.

        Args:

            :campus_id (optional[int, str]): Campus ID constraint.
            :buildings (optional[bool, str]): Include buildings.
            :sites (optional[bool, str]): Include sites.
            :aps (optional[bool, str]): Include access points.
            :messages (optional[bool, str]): Include messages.

        Returns:

            :Response: requests.models.Response.

        """
        url = self.api_path('visualrf/campus.xml')
        params_list = []
        if campus_id is not None:
            params_list.append('id=%s' % campus_id)
        for name, val in [('buildings', buildings), ('sites', sites), ('aps', aps), ('messages', messages)]:
            if val is not None:
                params_list.append('%s=%s' % (name, '' if val is True else val))
        params = '&'.join(params_list) if params_list else None
        return self.session.get(url, verify=self.verify, params=params)

    def visualrf_building(self, building_id=None, sites=None, aps=None, messages=None):
        """Query VisualRF building.

        Args:

            :building_id (optional[int, str]): Building ID constraint.
            :sites (optional[bool, str]): Include sites.
            :aps (optional[bool, str]): Include access points.
            :messages (optional[bool, str]): Include messages.

        Returns:

            :Response: requests.models.Response.

        """
        url = self.api_path('visualrf/building.xml')
        params_list = []
        if building_id is not None:
            params_list.append('id=%s' % building_id)
        for name, val in [('sites', sites), ('aps', aps), ('messages', messages)]:
            if val is not None:
                params_list.append('%s=%s' % (name, '' if val is True else val))
        params = '&'.join(params_list) if params_list else None
        return self.session.get(url, verify=self.verify, params=params)

    def visualrf_site(self, site_id=None, aps=None, messages=None):
        """Query VisualRF site.

        Args:

            :site_id (optional[str]): Site ID constraint.
            :aps (optional[bool, str]): Include access points.
            :messages (optional[bool, str]): Include messages.

        Returns:

            :Response: requests.models.Response.

        """
        url = self.api_path('visualrf/site.xml')
        params_list = []
        if site_id is not None:
            params_list.append('id=%s' % site_id)
        for name, val in [('aps', aps), ('messages', messages)]:
            if val is not None:
                params_list.append('%s=%s' % (name, '' if val is True else val))
        params = '&'.join(params_list) if params_list else None
        return self.session.get(url, verify=self.verify, params=params)

    def visualrf_access_point(self, ap_id=None, site_id=None):
        """Query VisualRF access point.

        Args:

            :ap_id (optional[int, str]): Access point ID constraint.
            :site_id (optional[str]): Site ID constraint.

        Returns:

            :Response: requests.models.Response.

        """
        url = self.api_path('visualrf/access_point.xml')
        params = {}
        if ap_id is not None:
            params['id'] = ap_id
        if site_id is not None:
            params['site_id'] = site_id
        params = AirWaveAPIClient.urlencode(params) if params else None
        return self.session.get(url, verify=self.verify, params=params)

    def visualrf_report(self, report_id=None, site_id=None):
        """Query VisualRF reports.

        Args:

            :report_id (optional[str]): Report ID constraint.
            :site_id (optional[str]): Site ID constraint.

        Returns:

            :Response: requests.models.Response.

        """
        url = self.api_path('visualrf/reports.xml')
        params = {}
        if report_id is not None:
            params['id'] = report_id
        if site_id is not None:
            params['site_id'] = site_id
        params = AirWaveAPIClient.urlencode(params) if params else None
        return self.session.get(url, verify=self.verify, params=params)

    def visualrf_rasterize(self, site_id=None, stats=False):
        """Generate or check VisualRF raster images status.

        Args:

            :site_id (optional[str]): Site ID to generate raster image for.
            :stats (bool): If True, view status of rasterization of sites. Default False.

        Returns:

            :Response: requests.models.Response.

        """
        url = self.api_path('visualrf/rasterize')
        params_list = []
        if site_id is not None:
            params_list.append('site_id=%s' % site_id)
        if stats:
            params_list.append('stats')
        params = '&'.join(params_list) if params_list else None
        return self.session.get(url, verify=self.verify, params=params)

    @staticmethod
    def id_params(ap_ids):
        """Make access point id string."""
        return '&'.join(["id=%s" % ap_id for ap_id in ap_ids])

    @staticmethod
    def urlencode(params):
        """URL Encode."""
        params = sorted(params.items())
        return urlencode(params)


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
        if 'ap' in data['amp:amp_ap_list']:
            obj = data['amp:amp_ap_list']['ap']
            aps = obj if isinstance(obj, list) else [obj]
            list.__init__(self, aps)

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
        if isinstance(obj, list):
            self.aps = obj
            OrderedDict.__init__(self, obj[0] if obj else {})
        else:
            self.aps = [obj]
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


class AMPStats(OrderedDict):

    """AMP Stats.

    This class inherits the OrderedDict class.

    """
    def __init__(self, xml):
        """Initialize AMPStats.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import AMPStats
            >>> res = airwave.amp_stats()
            >>> stats = AMPStats(res.text)
            >>> stats['up']
            '25'

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('amp_stats')), None)
        obj = data[root_key] if root_key and root_key in data else {}
        OrderedDict.__init__(self, obj)


class AlertList(list):

    """Alert List.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize AlertList.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import AlertList
            >>> res = airwave.alert_list()
            >>> alerts = AlertList(res.text)
            >>> for alert in alerts:
            ...     alert['@id']
            '83'

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('amp_alert')), None)
        records = []
        if root_key and 'record' in data[root_key]:
            raw = data[root_key]['record']
            records = raw if isinstance(raw, list) else [raw]
        list.__init__(self, records)

    def search(self, alert_id):
        """Search alert by ID.

        Args:

            :alert_id (int or str): Alert ID.

        Returns:

            :dict or None: Matching alert record dictionary.

        """
        target = str(alert_id)
        for record in self:
            if record.get('@id') == target or record.get('id') == target:
                return record
        return None


class APBSSIDList(list):

    """Access Point BSSID List.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize APBSSIDList.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import APBSSIDList
            >>> res = airwave.ap_bssid_list()
            >>> bssids = APBSSIDList(res.text)
            >>> node = bssids.search('AP 1')

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('amp_ap_bssid_list')), None)
        aps = []
        if root_key and 'ap' in data[root_key]:
            raw = data[root_key]['ap']
            aps = raw if isinstance(raw, list) else [raw]
        list.__init__(self, aps)

    def search(self, obj):
        """Search AP BSSID node by ID or name.

        Args:

            :obj (int or str): AP ID or AP name.

        Returns:

            :dict or None: Matching AP node dictionary.

        """
        if isinstance(obj, int):
            for ap in self:
                if int(ap.get('@id', -1)) == obj:
                    return ap
        elif isinstance(obj, str):
            for ap in self:
                if ap.get('@name') == obj or ap.get('name') == obj:
                    return ap
        return None


class APLog(list):

    """Access Point Log.

    This class inherits the list class containing log message records.

    """
    def __init__(self, xml):
        """Initialize APLog.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import APLog
            >>> res = airwave.ap_log([12, 13])
            >>> logs = APLog(res.text)
            >>> for entry in logs:
            ...     entry['@ap_id'], entry['message']

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('amp_ap_log')), None)
        entries = []
        if root_key and 'ap' in data[root_key]:
            raw_aps = data[root_key]['ap']
            ap_list = raw_aps if isinstance(raw_aps, list) else [raw_aps]
            for ap_node in ap_list:
                ap_id = ap_node.get('@id')
                if 'log_message' in ap_node:
                    msgs = ap_node['log_message']
                    msg_list = msgs if isinstance(msgs, list) else [msgs]
                    for msg in msg_list:
                        item = OrderedDict(msg)
                        item['@ap_id'] = ap_id
                        entries.append(item)
        list.__init__(self, entries)


class ClientDetail(OrderedDict):

    """Client Detail.

    This class inherits the OrderedDict class.

    """
    def __init__(self, xml):
        """Initialize ClientDetail.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import ClientDetail
            >>> res = airwave.client_detail('00:0E:35:52:8C:AB')
            >>> client = ClientDetail(res.text)
            >>> client['@mac']
            '00:0E:35:52:8C:AB'

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('amp_client_detail')), None)
        client_data = data[root_key]['client'] if root_key and 'client' in data[root_key] else {}
        if isinstance(client_data, list):
            self.clients = client_data
            primary = client_data[0] if client_data else {}
        else:
            self.clients = [client_data]
            primary = client_data
        OrderedDict.__init__(self, primary)


class UserInfo(OrderedDict):

    """User Info.

    This class inherits the OrderedDict class.

    """
    def __init__(self, xml):
        """Initialize UserInfo.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import UserInfo
            >>> res = airwave.user_info()
            >>> user = UserInfo(res.text)
            >>> user['username']
            'admin'

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('amp_user_info')), None)
        user_data = data[root_key]['user'] if root_key and 'user' in data[root_key] else {}
        OrderedDict.__init__(self, user_data)


class Topology(list):

    """Topology List.

    This class inherits the list class containing device nodes in a folder.

    """
    def __init__(self, data):
        """Initialize Topology.

        Args:

            :data (str, bytes, or dict): JSON string or parsed dictionary.

        Usage: ::

            >>> from airwaveapiclient import Topology
            >>> res = airwave.topology_list(5)
            >>> topology = Topology(res.text)
            >>> for node in topology:
            ...     node['apID'], node['name']

        """
        if isinstance(data, (str, bytes)):
            raw_data = json.loads(data)
        elif isinstance(data, dict):
            raw_data = data
        else:
            raw_data = {}

        self.raw = raw_data
        nodes = raw_data.get('nodes', [])
        if not isinstance(nodes, list):
            nodes = [nodes] if nodes else []
        list.__init__(self, nodes)

    def search(self, obj):
        """Search node by AP ID, name, or MAC address.

        Args:

            :obj (int or str): AP ID, name, or MAC address.

        Returns:

            :dict or None: Matching device node dictionary.

        """
        if isinstance(obj, int):
            for node in self:
                if node.get('apID') == obj:
                    return node
        elif isinstance(obj, str):
            clean = obj.strip().lower()
            if clean.isdigit():
                target_id = int(clean)
                for node in self:
                    if node.get('apID') == target_id:
                        return node
            for node in self:
                if str(node.get('name', '')).lower() == clean or str(node.get('mac', '')).lower() == clean:
                    return node
        return None


class ConfigResult(OrderedDict):

    """Configuration API Result.

    This class inherits the OrderedDict class.

    """
    def __init__(self, data):
        """Initialize ConfigResult.

        Args:

            :data (str, bytes, or dict): JSON string, plain text, or dictionary.

        Usage: ::

            >>> from airwaveapiclient import ConfigResult
            >>> res = airwave.add_ssl_certificate(cert_data, passphrase)
            >>> result = ConfigResult(res.text)
            >>> result.status
            'PKCS12 bundle extraction successful...'

        """
        res_dict = OrderedDict()
        if isinstance(data, dict):
            res_dict.update(data)
        elif isinstance(data, (str, bytes)):
            text = data.decode('utf-8') if isinstance(data, bytes) else data
            text_strip = text.strip()
            if text_strip.startswith('{') and text_strip.endswith('}'):
                try:
                    res_dict.update(json.loads(text_strip, object_pairs_hook=OrderedDict))
                except Exception:
                    res_dict['message'] = text_strip
            else:
                res_dict['message'] = text_strip
        self.message = res_dict.get('message') or res_dict.get('status') or ''
        self.status = res_dict.get('status') or self.message
        low = self.message.lower()
        self.success = 'fail' not in low and 'error' not in low and 'denied' not in low and 'invalid' not in low
        OrderedDict.__init__(self, res_dict)


class FolderList(list):

    """Folder List.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize FolderList.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import FolderList
            >>> res = airwave.folder_list()
            >>> folders = FolderList(res.text)
            >>> folder = folders.search(1)

        """
        data = xmltodict.parse(xml)
        if 'folder' in data['amp:amp_folder_list']:
            obj = data['amp:amp_folder_list']['folder']
            folders = obj if isinstance(obj, list) else [obj]
            list.__init__(self, folders)

    def search(self, folder_id):
        """Search Folder by ID.

        Args:

            :folder_id (int or str): Folder ID.

        Returns:

            :dict or None: Matching folder dictionary.

        """
        target = str(folder_id)
        for folder in self:
            if folder.get('@id') == target or folder.get('id') == target:
                return folder
        return None


class APSearch(list):

    """Access Point Search Results.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize APSearch.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import APSearch
            >>> res = airwave.ap_search('00:0B:85:1B:A6:90')
            >>> results = APSearch(res.text)
            >>> record = results.search('3647')

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('amp_ap_search')), None)
        records = []
        if root_key and 'record' in data[root_key]:
            raw = data[root_key]['record']
            records = raw if isinstance(raw, list) else [raw]
        list.__init__(self, records)

    def search(self, obj):
        """Search record by ID or name.

        Args:

            :obj (int or str): Record ID or name.

        Returns:

            :dict or None: Matching search record dictionary.

        """
        target = str(obj).lower()
        for rec in self:
            if str(rec.get('@id', '')).lower() == target or str(rec.get('id', '')).lower() == target:
                return rec
            name_val = rec.get('name')
            if isinstance(name_val, dict):
                if str(name_val.get('#text', '')).lower() == target or str(name_val.get('@sort_value', '')).lower() == target:
                    return rec
            elif isinstance(name_val, str) and name_val.lower() == target:
                return rec
        return None


class ClientSearch(list):

    """Client Search Results.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize ClientSearch.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import ClientSearch
            >>> res = airwave.client_search('00:0E:35:52:8C:AB')
            >>> results = ClientSearch(res.text)

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('amp_client_search')), None)
        records = []
        if root_key and 'record' in data[root_key]:
            raw = data[root_key]['record']
            records = raw if isinstance(raw, list) else [raw]
        list.__init__(self, records)

    def search(self, obj):
        """Search record by ID, MAC, or username.

        Args:

            :obj (int or str): Record ID, MAC address, or username.

        Returns:

            :dict or None: Matching search record dictionary.

        """
        target = str(obj).lower()
        for rec in self:
            if str(rec.get('@id', '')).lower() == target or str(rec.get('id', '')).lower() == target:
                return rec
            for key in ('mac', 'username'):
                val = rec.get(key)
                if isinstance(val, dict):
                    if str(val.get('#text', '')).lower() == target or str(val.get('@sort_value', '')).lower() == target or str(val.get('@ascii_value', '')).lower() == target:
                        return rec
                elif isinstance(val, str) and val.lower() == target:
                    return rec
        return None


class VPNUserSearch(list):

    """VPN User Search Results.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize VPNUserSearch.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import VPNUserSearch
            >>> res = airwave.vpn_user_search('photocrayon')
            >>> results = VPNUserSearch(res.text)

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('amp_vpn_user_search')), None)
        records = []
        if root_key and 'record' in data[root_key]:
            raw = data[root_key]['record']
            records = raw if isinstance(raw, list) else [raw]
        list.__init__(self, records)

    def search(self, obj):
        """Search record by ID or username / userid.

        Args:

            :obj (int or str): Record ID or userid.

        Returns:

            :dict or None: Matching search record dictionary.

        """
        target = str(obj).lower()
        for rec in self:
            if str(rec.get('@id', '')).lower() == target or str(rec.get('id', '')).lower() == target:
                return rec
            for key in ('userid', 'username'):
                val = rec.get(key)
                if isinstance(val, dict):
                    if str(val.get('#text', '')).lower() == target or str(val.get('@sort_value', '')).lower() == target or str(val.get('@ascii_value', '')).lower() == target:
                        return rec
                elif isinstance(val, str) and val.lower() == target:
                    return rec
        return None


class RogueDetail(OrderedDict):

    """Rogue Access Point Detail.

    This class inherits the OrderedDict class.

    """
    def __init__(self, xml):
        """Initialize RogueDetail.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import RogueDetail
            >>> res = airwave.rogue_detail(495)
            >>> rogue = RogueDetail(res.text)

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('amp_rogue_detail')), None)
        rogue_data = data[root_key]['rogue_ap'] if root_key and 'rogue_ap' in data[root_key] else {}
        OrderedDict.__init__(self, rogue_data)


class ClientLocation(OrderedDict):

    """Client Location in VisualRF.

    This class inherits the OrderedDict class.

    """
    def __init__(self, xml):
        """Initialize ClientLocation.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import ClientLocation
            >>> res = airwave.client_location('12:34:56:78:90:AB')
            >>> loc = ClientLocation(res.text)

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('location')), None)
        loc_data = data[root_key] if root_key else {}
        OrderedDict.__init__(self, loc_data)


class VisualRFCampus(list):

    """VisualRF Campus List.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize VisualRFCampus.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import VisualRFCampus
            >>> res = airwave.visualrf_campus()
            >>> campuses = VisualRFCampus(res.text)

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('campuses')), None)
        campuses = []
        if root_key and 'campus' in data[root_key]:
            raw = data[root_key]['campus']
            campuses = raw if isinstance(raw, list) else [raw]
        list.__init__(self, campuses)

    def search(self, obj):
        """Search campus by ID or name.

        Args:

            :obj (int or str): Campus ID or name.

        Returns:

            :dict or None: Matching campus dictionary.

        """
        target = str(obj).lower()
        for c in self:
            if str(c.get('@id', '')).lower() == target or str(c.get('@name', '')).lower() == target or str(c.get('name', '')).lower() == target:
                return c
        return None


class VisualRFBuilding(list):

    """VisualRF Building List.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize VisualRFBuilding.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import VisualRFBuilding
            >>> res = airwave.visualrf_building()
            >>> buildings = VisualRFBuilding(res.text)

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('buildings')), None)
        buildings = []
        if root_key and 'building' in data[root_key]:
            raw = data[root_key]['building']
            buildings = raw if isinstance(raw, list) else [raw]
        list.__init__(self, buildings)

    def search(self, obj):
        """Search building by ID or name.

        Args:

            :obj (int or str): Building ID or name.

        Returns:

            :dict or None: Matching building dictionary.

        """
        target = str(obj).lower()
        for b in self:
            if str(b.get('@id', '')).lower() == target or str(b.get('@name', '')).lower() == target or str(b.get('name', '')).lower() == target:
                return b
        return None


class VisualRFSite(list):

    """VisualRF Site List.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize VisualRFSite.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import VisualRFSite
            >>> res = airwave.visualrf_site()
            >>> sites = VisualRFSite(res.text)

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('sites')), None)
        sites = []
        if root_key and 'site' in data[root_key]:
            raw = data[root_key]['site']
            sites = raw if isinstance(raw, list) else [raw]
        list.__init__(self, sites)

    def search(self, obj):
        """Search site by ID or name.

        Args:

            :obj (int or str): Site ID or name.

        Returns:

            :dict or None: Matching site dictionary.

        """
        target = str(obj).lower()
        for s in self:
            if str(s.get('@id', '')).lower() == target or str(s.get('@name', '')).lower() == target or str(s.get('name', '')).lower() == target:
                return s
        return None


class VisualRFAccessPoint(list):

    """VisualRF Access Point List.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize VisualRFAccessPoint.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import VisualRFAccessPoint
            >>> res = airwave.visualrf_access_point()
            >>> aps = VisualRFAccessPoint(res.text)

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('site_access_points')), None)
        aps = []
        if root_key and 'ap' in data[root_key]:
            raw = data[root_key]['ap']
            aps = raw if isinstance(raw, list) else [raw]
        list.__init__(self, aps)

    def search(self, obj):
        """Search access point by ID or name.

        Args:

            :obj (int or str): AP ID or name.

        Returns:

            :dict or None: Matching access point dictionary.

        """
        target = str(obj).lower()
        for ap in self:
            if str(ap.get('@id', '')).lower() == target or str(ap.get('@name', '')).lower() == target or str(ap.get('name', '')).lower() == target:
                return ap
        return None


class VisualRFReport(list):

    """VisualRF Report List.

    This class inherits the list class.

    """
    def __init__(self, xml):
        """Initialize VisualRFReport.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import VisualRFReport
            >>> res = airwave.visualrf_report()
            >>> reports = VisualRFReport(res.text)

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith('reports')), None)
        reports = []
        if root_key and 'report' in data[root_key]:
            raw = data[root_key]['report']
            reports = raw if isinstance(raw, list) else [raw]
        list.__init__(self, reports)

    def search(self, obj):
        """Search report by ID or name.

        Args:

            :obj (int or str): Report ID or name.

        Returns:

            :dict or None: Matching report dictionary.

        """
        target = str(obj).lower()
        for r in self:
            if str(r.get('@id', '')).lower() == target or str(r.get('@name', '')).lower() == target or str(r.get('name', '')).lower() == target:
                return r
        return None


class VisualRFRasterize(OrderedDict):

    """VisualRF Rasterize Result.

    This class inherits the OrderedDict class.

    """
    def __init__(self, xml):
        """Initialize VisualRFRasterize.

        Args:

            :xml (str): XML string.

        Usage: ::

            >>> from airwaveapiclient import VisualRFRasterize
            >>> res = airwave.visualrf_rasterize()
            >>> raster = VisualRFRasterize(res.text)

        """
        data = xmltodict.parse(xml)
        root_key = next((k for k in data if k.endswith(('images', 'sites'))), None)
        obj = data[root_key] if root_key else {}
        self.images = []
        self.sites = []
        if 'image' in obj:
            raw = obj['image']
            self.images = raw if isinstance(raw, list) else [raw]
        if 'site' in obj:
            raw = obj['site']
            self.sites = raw if isinstance(raw, list) else [raw]
        OrderedDict.__init__(self, obj)

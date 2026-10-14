# -*- coding: utf-8 -*-

"""UnitTests for airwaveapiclient."""

import unittest
from httmock import all_requests, response, HTTMock
from airwaveapiclient import AirWaveAPIClient


# pylint: disable=unused-argument
# pylint: disable=too-many-instance-attributes
# pylint: disable=protected-access
class AirWaveAPIClientUnitTests(unittest.TestCase):

    """Class AirWaveAPIClientUnitTests.

    Unit test for airwaveapiclient.

    """

    def setUp(self):
        """Setup."""
        self.username = 'username'
        self.password = 'password'
        self.url = 'https://192.168.1.1'

        self.obj = AirWaveAPIClient(username=self.username,
                                    password=self.password,
                                    url=self.url)

        with HTTMock(AirWaveAPIClientUnitTests.content_login):
            self.res = self.obj.login()

    def tearDown(self):
        """Tear down."""
        self.obj.logout()

    def test_init(self):
        """Test init."""
        self.assertEqual(self.obj.username, self.username)
        self.assertEqual(self.obj.password, self.password)
        self.assertEqual(self.obj.url, self.url)
        self.assertNotEqual(self.obj.session, None)

    def test_api_path(self):
        """Test API path."""
        path = 'ap_list.xml'
        url = self.obj.api_path(path)
        self.assertEqual(url, '%s/%s' % (self.url, path))

    def test_id_params(self):
        """Test ID Params."""
        ap_ids = [1, 2, 3]
        params = self.obj.id_params(ap_ids)
        self.assertEqual(params, 'id=1&id=2&id=3')

    def test_urlencode(self):
        """Test urlencode."""
        params = {'mac': '12:34:56:78:90:AB'}
        res = self.obj.urlencode(params)
        self.assertEqual(res, 'mac=12%3A34%3A56%3A78%3A90%3AAB')

    def test_login(self):
        """Test login."""
        self.assertEqual(self.res.status_code, 200)

    def test_logout(self):
        """Test logout."""
        self.assertEqual(self.obj.logout(), None)

    def test_ap_list(self):
        """Test ap_list."""
        path_ap_list = 'ap_list.xml'

        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.ap_list()
        self.assertEqual(res.status_code, 200)

        url = '%s/%s' % (self.url, path_ap_list)
        self.assertEqual(res.url, url)

        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            ap_ids = [1, 2, 3]
            res = self.obj.ap_list(ap_ids)
        self.assertEqual(res.status_code, 200)

        params = self.obj.id_params(ap_ids)
        url = '%s/%s?%s' % (self.url, path_ap_list, params)
        self.assertEqual(res.url, url)

    def test_ap_detail(self):
        """Test ap_detail."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            ap_id = 1
            res = self.obj.ap_detail(ap_id)
        self.assertEqual(res.status_code, 200)

        path_ap_detail = 'ap_detail.xml'
        ap_ids = [ap_id]
        params = self.obj.id_params(ap_ids)
        url = '%s/%s?%s' % (self.url, path_ap_detail, params)
        self.assertEqual(res.url, url)

        # Multi-ID ap_detail
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            multi_ids = [1, 2, 3]
            res = self.obj.ap_detail(multi_ids)
        self.assertEqual(res.status_code, 200)
        params_multi = self.obj.id_params(multi_ids)
        url_multi = '%s/%s?%s' % (self.url, path_ap_detail, params_multi)
        self.assertEqual(res.url, url_multi)

    def test_ap_search(self):
        """Test ap_search."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            query = '00:0B:85:1B:A6:90'
            res = self.obj.ap_search(query)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s/ap_search.xml?query=00%%3A0B%%3A85%%3A1B%%3AA6%%3A90' % self.url)

    def test_folder_list(self):
        """Test folder_list."""
        path_folder_list = 'folder_list.xml'

        # All folders
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.folder_list()
        self.assertEqual(res.status_code, 200)
        url = '%s/%s' % (self.url, path_folder_list)
        self.assertEqual(res.url, url)

        # Multiple IDs folder_list
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            folder_ids = [10, 20]
            res = self.obj.folder_list(folder_ids)
        self.assertEqual(res.status_code, 200)
        params = self.obj.id_params(folder_ids)
        url = '%s/%s?%s' % (self.url, path_folder_list, params)
        self.assertEqual(res.url, url)

        # Single ID integer
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.folder_list(10)
        self.assertEqual(res.status_code, 200)
        url = '%s/%s?id=10' % (self.url, path_folder_list)
        self.assertEqual(res.url, url)

        # Single ID string
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.folder_list('20')
        self.assertEqual(res.status_code, 200)
        url = '%s/%s?id=20' % (self.url, path_folder_list)
        self.assertEqual(res.url, url)

    def test_client_detail(self):
        """Test client detail."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            mac = '12:34:56:78:90:AB'
            params = {'mac': mac}
            params = self.obj.urlencode(params)
            res = self.obj.client_detail(mac)
        self.assertEqual(res.status_code, 200)

        path_client_detail = 'client_detail.xml'
        url = '%s/%s?%s' % (self.url, path_client_detail, params)
        self.assertEqual(res.url, url)

    def test_client_search(self):
        """Test client_search."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            query = '00:0E:35:52:8C:AB'
            res = self.obj.client_search(query)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s/client_search.xml?query=00%%3A0E%%3A35%%3A52%%3A8C%%3AAB' % self.url)

    def test_client_location(self):
        """Test client_location."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            mac = '12:34:56:78:90:AB'
            res = self.obj.client_location(mac)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s/visualrf/location.xml?mac=12%%3A34%%3A56%%3A78%%3A90%%3AAB' % self.url)

    def test_rogue_detail(self):
        """Test rogue detail."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            ap_id = 1
            params = {'id': ap_id}
            params = self.obj.urlencode(params)
            res = self.obj.rogue_detail(ap_id)
        self.assertEqual(res.status_code, 200)

        path_rogue_detail = 'rogue_detail.xml'
        url = '%s/%s?%s' % (self.url, path_rogue_detail, params)
        self.assertEqual(res.url, url)

    def test_latest_report(self):
        """Test latest report."""
        report_id = 1
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.latest_report(report_id)
        self.assertEqual(res.status_code, 200)

        path_latest_report = 'latest_report.xml'
        params = {'id': report_id}
        params = self.obj.urlencode(params)
        url = '%s/%s?%s' % (self.url, path_latest_report, params)
        self.assertEqual(res.url, url)

    def test_biscotti_auth(self):
        """Test X-BISCOTTI token capture and header propagation."""
        self.assertEqual(self.obj.biscotti, 'test_biscotti_token')
        self.assertEqual(self.obj.session.headers.get('X-BISCOTTI'), 'test_biscotti_token')

        # Custom token in constructor
        client = AirWaveAPIClient(username='user', password='pwd', url=self.url, biscotti='custom_token')
        self.assertEqual(client.biscotti, 'custom_token')
        self.assertEqual(client.session.headers.get('X-BISCOTTI'), 'custom_token')

        # Logout clears token
        client.logout()
        self.assertIsNone(client.biscotti)

    def test_is_cred_obfusc_enabled(self):
        """Test is_cred_obfusc when enabled."""
        @all_requests
        def mock_obfusc_enabled(url, request):
            if 'is_cred_obfusc.json' in url.path:
                return response(200, '{"is_cred_obfuscation": 1}', {'content-type': 'application/json'}, request=request)
            return response(404, request=request)

        with HTTMock(mock_obfusc_enabled):
            self.assertTrue(self.obj.is_cred_obfusc())

    def test_is_cred_obfusc_disabled(self):
        """Test is_cred_obfusc when disabled."""
        @all_requests
        def mock_obfusc_disabled(url, request):
            if 'is_cred_obfusc.json' in url.path:
                return response(200, '{"is_cred_obfuscation": 0}', {'content-type': 'application/json'}, request=request)
            return response(404, request=request)

        with HTTMock(mock_obfusc_disabled):
            self.assertFalse(self.obj.is_cred_obfusc())

    def test_is_cred_obfusc_fallback(self):
        """Test is_cred_obfusc fallback on 404 or connection error."""
        @all_requests
        def mock_404(url, request):
            return response(404, 'Not Found', request=request)

        with HTTMock(mock_404):
            self.assertFalse(self.obj.is_cred_obfusc())

    def test_login_with_obfuscation(self):
        """Test login automatically base64-encodes password when obfuscation is enabled."""
        captured_data = {}

        @all_requests
        def mock_flow(url, request):
            if 'is_cred_obfusc.json' in url.path:
                return response(200, '{"is_cred_obfuscation": 1}', {'content-type': 'application/json'}, request=request)
            if 'LOGIN' in url.path:
                captured_data['body'] = request.body
                return response(200, '<html>ok</html>', {'X-BISCOTTI': 'obfusc_token'}, request=request)
            return response(404, request=request)

        client = AirWaveAPIClient(username='admin', password='mypassword', url=self.url)
        with HTTMock(mock_flow):
            res = client.login()
        self.assertEqual(res.status_code, 200)
        import base64
        expected_pwd = base64.b64encode(b'mypassword').decode('utf-8')
        from urllib.parse import quote_plus
        self.assertIn('credential_1=%s' % quote_plus(expected_pwd), captured_data['body'])

    def test_login_without_obfuscation(self):
        """Test login uses plain text password when obfuscation is unsupported."""
        captured_data = {}

        @all_requests
        def mock_flow(url, request):
            if 'is_cred_obfusc.json' in url.path:
                return response(404, 'Not Found', request=request)
            if 'LOGIN' in url.path:
                captured_data['body'] = request.body
                return response(200, '<html>ok</html>', {'X-BISCOTTI': 'plain_token'}, request=request)
            return response(404, request=request)

        client = AirWaveAPIClient(username='admin', password='mypassword', url=self.url)
        with HTTMock(mock_flow):
            res = client.login()
        self.assertEqual(res.status_code, 200)
        self.assertIn('credential_1=mypassword', captured_data['body'])

    def test_ap_detail_filters(self):
        """Test ap_detail with folder_id, group_id, controller_id, and optional ap_ids."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res_all = self.obj.ap_detail()
            res_filtered = self.obj.ap_detail(folder_id=10, group_id=2, controller_id=1)
            res_with_id = self.obj.ap_detail(123, folder_id=10)
        self.assertEqual(res_all.url, '%s/ap_detail.xml' % self.url)
        self.assertEqual(res_filtered.url, '%s/ap_detail.xml?ap_folder_id=10&ap_group_id=2&controller_id=1' % self.url)
        self.assertEqual(res_with_id.url, '%s/ap_detail.xml?id=123&ap_folder_id=10' % self.url)

    def test_alert_list(self):
        """Test alert_list."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.alert_list()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s/alerts.xml' % self.url)

    def test_ap_bssid_list(self):
        """Test ap_bssid_list."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.ap_bssid_list([123, 124], folder_id=10)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s/api/ap_bssid_list.xml?id=123&id=124&ap_folder_id=10' % self.url)

    def test_ap_log(self):
        """Test ap_log."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.ap_log([12, 13], limit=10)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s/ap_log.xml?id=12&id=13&limit=10' % self.url)

    def test_user_info(self):
        """Test user_info."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.user_info()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s/user_info.xml' % self.url)

    def test_topology_list(self):
        """Test topology_list."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.topology_list(5)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s/topology/getTopology?folderId=5' % self.url)

        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.topology_list()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s/topology/getTopology?folderId=' % self.url)

    def test_vpn_user_search(self):
        """Test vpn_user_search."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.vpn_user_search('photocrayon')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s/vpn_user_search.xml?query=photocrayon' % self.url)

    def test_device_management(self):
        """Test device management APIs (delete, move folder, move group)."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res_del = self.obj.delete_device(1)
            res_mf = self.obj.move_to_folder(1, 2)
            res_mg = self.obj.move_to_group(10, group_id=1, group_name='AP Group')
        self.assertEqual(res_del.status_code, 200)
        self.assertEqual(res_del.url, '%s/api/delete_device' % self.url)
        self.assertEqual(res_mf.status_code, 200)
        self.assertEqual(res_mf.url, '%s/api/move_to_folder' % self.url)
        self.assertEqual(res_mg.status_code, 200)
        self.assertEqual(res_mg.url, '%s/api/move_to_group' % self.url)

    def test_config_apis(self):
        """Test config APIs (allowlist upload, template variable, ssl certificate)."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res_al = self.obj.ap_allowlist_upload('csv_data', append_allowlist=1)
            res_tv = self.obj.template_variable_update('<xml/>')
            res_ssl = self.obj.add_ssl_certificate('cert_data', 'passphrase')
        self.assertEqual(res_al.status_code, 200)
        self.assertEqual(res_al.url, '%s/api/ap_allowlist_upload' % self.url)
        self.assertEqual(res_tv.status_code, 200)
        self.assertEqual(res_tv.url, '%s/template_variable_api' % self.url)
        self.assertEqual(res_ssl.status_code, 200)
        self.assertEqual(res_ssl.url, '%s/api/add_ssl_certificate' % self.url)

    def test_visualrf_apis(self):
        """Test VisualRF APIs."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res_c = self.obj.visualrf_campus(3, buildings=True, sites=True)
            res_b = self.obj.visualrf_building(15, aps=True)
            res_s = self.obj.visualrf_site('site_guid')
            res_ap = self.obj.visualrf_access_point(12660)
            res_r = self.obj.visualrf_report('rep_guid')
            res_ras = self.obj.visualrf_rasterize('site_guid', stats=True)
        self.assertEqual(res_c.status_code, 200)
        self.assertEqual(res_c.url, '%s/visualrf/campus.xml?id=3&buildings=&sites=' % self.url)
        self.assertEqual(res_b.status_code, 200)
        self.assertEqual(res_b.url, '%s/visualrf/building.xml?id=15&aps=' % self.url)
        self.assertEqual(res_s.status_code, 200)
        self.assertEqual(res_s.url, '%s/visualrf/site.xml?id=site_guid' % self.url)
        self.assertEqual(res_ap.status_code, 200)
        self.assertEqual(res_ap.url, '%s/visualrf/access_point.xml?id=12660' % self.url)
        self.assertEqual(res_r.status_code, 200)
        self.assertEqual(res_r.url, '%s/visualrf/reports.xml?id=rep_guid' % self.url)
        self.assertEqual(res_ras.status_code, 200)
        self.assertEqual(res_ras.url, '%s/visualrf/rasterize?site_id=site_guid&stats' % self.url)

    def test_extended_parameters(self):
        """Test extended parameters on existing APIs."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res_stats = self.obj.amp_stats(include_all_stats=True, include_bandwidth=True)
            res_ap = self.obj.ap_list(folder_id=5, group_id=2, controller_id=1)
            res_detail = self.obj.ap_detail(123, include_ignored=True)
            res_client = self.obj.client_detail('12:34:56:78:90:AB', limit=5)
            res_rogue = self.obj.rogue_detail(123, limit=10)
        self.assertEqual(res_stats.status_code, 200)
        self.assertEqual(res_stats.url, '%s/amp_stats.xml?include_all_stats=1&include_bandwidth=1' % self.url)
        self.assertEqual(res_ap.status_code, 200)
        self.assertEqual(res_ap.url, '%s/ap_list.xml?ap_folder_id=5&ap_group_id=2&controller_id=1' % self.url)
        self.assertEqual(res_detail.status_code, 200)
        self.assertEqual(res_detail.url, '%s/ap_detail.xml?id=123&include=ignored' % self.url)
        self.assertEqual(res_client.status_code, 200)
        self.assertEqual(res_client.url, '%s/client_detail.xml?limit=5&mac=12%%3A34%%3A56%%3A78%%3A90%%3AAB' % self.url)
        self.assertEqual(res_rogue.status_code, 200)
        self.assertEqual(res_rogue.url, '%s/rogue_detail.xml?id=123&limit=10' % self.url)

    @staticmethod
    @all_requests
    def content_login(url, request):
        """Test content for login."""
        cookie_key = 'Mercury::Handler::AuthCookieHandler_AMPAuth'
        cookie_val = '01234567890abcdef01234567890abcd'
        headers = {'Set-Cookie': '%s=%s;' % (cookie_key, cookie_val),
                   'X-BISCOTTI': 'test_biscotti_token'}
        content = '<html>html content.</html>'
        return response(status_code=200,
                        content=content,
                        headers=headers,
                        request=request)

    @staticmethod
    @all_requests
    def content_api_xml(url, request):
        """Test content for api xml."""
        headers = {'content-type': 'application/xml'}
        content = 'xml string'
        return response(status_code=200,
                        content=content,
                        headers=headers,
                        request=request)

    @staticmethod
    @all_requests
    def content_api_xhtml(url, request):
        """Test content for api xhtml."""
        headers = {'content-type': 'application/xhtml'}
        content = 'xhtml string'
        return response(status_code=200,
                        content=content,
                        headers=headers,
                        request=request)

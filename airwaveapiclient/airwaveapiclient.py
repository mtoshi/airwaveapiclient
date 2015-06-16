# -*- coding: utf-8 -*-

"""airwaveapiclient."""


import requests


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

    @staticmethod
    def id_params(ap_ids):
        """Make access point id dict. """
        return '&'.join(["id=%s" % ap_id for ap_id in ap_ids])

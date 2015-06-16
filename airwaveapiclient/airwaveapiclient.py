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

    def ap_list(self):
        """Get Access Point list."""
        url = self.api_path('ap_list.xml')
        query = '<access_points><ap /></access_points>'
        params = {'aps': query}
        return self.session.post(url,
                                 params=params,
                                 verify=False)

    def ap_detail(self, ap_id):
        """Get Access Point detail."""
        url = self.api_path('ap_list.xml')  # "ap_detail.xml" could not use.
        query = '<access_points><ap id="%s" /></access_points>' % ap_id
        params = {'aps': query}
        return self.session.post(url,
                                 params=params,
                                 verify=False)

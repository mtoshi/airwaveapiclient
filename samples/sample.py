# -*- coding: utf-8 -*-

"""AirWaveAPIClient sample."""


from airwaveapiclient import AirWaveAPIClient
from airwaveapiclient import APList
from airwaveapiclient import APDetail
from pprint import pprint


def main():
    """Sample main."""
    #################################################
    # Settings ######################################
    #################################################

    username = 'admin'
    password = '*****'
    url = 'https://192.168.1.1'

    #################################################
    # Login #########################################
    #################################################

    airwave = AirWaveAPIClient(username=username,
                               password=password,
                               url=url)
    airwave.login()

    #################################################
    # APList ########################################
    #################################################

    res = airwave.ap_list()
    if res.status_code == 200:
        xml = res.text
        ap_list = APList(xml)
        for ap_node in ap_list:
            pprint(ap_node)

    #################################################
    # APDetail ######################################
    #################################################

    for ap_node in ap_list:
        res = airwave.ap_detail(ap_node['@id'])
        if res.status_code == 200:
            xml = res.text
            ap_detail = APDetail(xml)
            pprint(ap_detail)

    #################################################
    # Logout ########################################
    #################################################

    airwave.logout()

if __name__ == "__main__":

    main()

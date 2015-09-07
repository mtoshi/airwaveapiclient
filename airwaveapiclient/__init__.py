# -*- coding: utf-8 -*-

"""airwaveapiclient."""

import sys

# pylint: disable=unused-import,import-error,relative-import,no-name-in-module
if sys.version_info.major == 2:
    from airwaveapiclient import AirWaveAPIClient
    from airwaveapiclient import APList
    from airwaveapiclient import APDetail
    from airwaveapiclient import Report
    from ap_graph import APGraph

else:
    from airwaveapiclient.airwaveapiclient import AirWaveAPIClient
    from airwaveapiclient.airwaveapiclient import APList
    from airwaveapiclient.airwaveapiclient import APDetail
    from airwaveapiclient.airwaveapiclient import Report
    from airwaveapiclient.ap_graph import APGraph

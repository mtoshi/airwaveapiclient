# -*- coding: utf-8 -*-

"""airwaveapiclient."""

import sys

# pylint: disable=unused-import
if sys.version_info.major == 2:
    from airwaveapiclient import AirWaveAPIClient
    from airwaveapiclient import APList
    from airwaveapiclient import APNode
else:
    from airwaveapiclient.airwaveapiclient import AirWaveAPIClient
    from airwaveapiclient.airwaveapiclient import APList
    from airwaveapiclient.airwaveapiclient import APNode

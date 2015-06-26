# -*- coding: utf-8 -*-

"""airwaveapiclient."""

import sys

# pylint: disable=unused-import
if sys.version_info.major == 2:
    from airwaveapiclient import AirWaveAPIClient
else:
    from airwaveapiclient.airwaveapiclient import AirWaveAPIClient

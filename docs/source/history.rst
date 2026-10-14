History
============

0.1.12 (2026-10-13)
-------------------
* Add full X-BISCOTTI token authentication and header session support.
* Add automatic credential obfuscation support with transparent fallback for older AirWave versions.
* Add missing AirWave Query APIs: alert_list, ap_bssid_list, ap_log, user_info, topology_list.
* Add missing AirWave Search API: vpn_user_search.
* Add missing AirWave Configuration APIs: delete_device, move_to_folder, move_to_group, ap_allowlist_upload, template_variable_update, add_ssl_certificate.
* Add missing AirWave VisualRF APIs: visualrf_campus, visualrf_building, visualrf_site, visualrf_access_point, visualrf_report, visualrf_rasterize.
* Extend AirWaveAPIClient.folder_list to support multiple folder IDs in a single query.
* Extend AirWaveAPIClient.ap_detail to support multiple AP IDs, include_ignored flag, and filtering by folder_id, group_id, and controller_id.
* Extend client_detail, rogue_detail, amp_stats, and ap_list with documented parameters.
* Add response models for all endpoints: AMPStats, AlertList, APBSSIDList, APLog, ClientDetail, UserInfo, Topology, ConfigResult, FolderList, APSearch, ClientSearch, VPNUserSearch, RogueDetail, ClientLocation, VisualRFCampus, VisualRFBuilding, VisualRFSite, VisualRFAccessPoint, VisualRFReport, VisualRFRasterize.
* Add unit tests with standalone fixtures for all response models and all client methods.
* Update APDetail to handle multi-AP responses.
* Fix urlencode compatibility with urllib3 2.0+.
* Add pyproject.toml and requirements.txt for modern PEP 517/518 build and pip installation.
* Drop Python 2 support (requires Python >= 3.6).

0.1.11 (2019-06-12)
-------------------
* Add client_search, ap_search and client_location methods.

0.1.10 (2018-08-25)
-------------------
* Minor change for reliability.

0.1.9 (2017-10-13)
------------------
* Change method to generate URL path.

0.1.8 (2017-06-30)
------------------
* Added AMP stats and folder list methods.
* Changed documentation.

0.1.7 (2015-09-14)
------------------
* Changed some structures for stable into the APGraph methods.
* Changed documentation.

0.1.6 (2015-09-09)
------------------
* Added care of non existent graph url.
* Changed documentation.

0.1.5 (2015-09-07)
------------------
* Changed documentation.

0.1.4 (2015-09-07)
------------------
* Added latest report API.
* Changed documentation.

0.1.3 (2015-08-17)
------------------
* Added 802.11ac graph url.
* Changed documentation.

0.1.2 (2015-08-03)
------------------
* Changed documentation.

0.1.1 (2015-08-02)
------------------
* Changed documentation.

0.1.0 (2015-08-01)
------------------
* First release

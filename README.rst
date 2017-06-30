===================================================
airwaveapiclient
===================================================

Airwaveapiclient is a utility tool for Aruba Networks AirWave users.
This module connects to AirWave and gets the information such as the access point list,
detail, client, etc.

.. image:: https://secure.travis-ci.org/mtoshi/airwaveapiclient.svg?branch=master
   :target: http://travis-ci.org/mtoshi/airwaveapiclient
.. image:: https://coveralls.io/repos/mtoshi/airwaveapiclient/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/mtoshi/airwaveapiclient?branch=master
.. image:: https://img.shields.io/pypi/v/airwaveapiclient.svg
   :target: https://pypi.python.org/pypi/airwaveapiclient
   :alt: Latest Version
.. image:: https://readthedocs.org/projects/airwaveapiclient/badge/?version=latest
   :target: https://airwaveapiclient.readthedocs.org
   :alt: Documentation Status

Requirements
============
* Python2.7, 3.4, PyPy.

Installation
============
* PyPI or Github ::

   $ pip install airwaveapiclient

   or

   $ git clone https://github.com/mtoshi/airwaveapiclient
   $ cd airwaveapiclient
   $ sudo python setup.py install


Using example
=============
* Documentation: Readthedocs_
    .. _Readthedocs: https://airwaveapiclient.readthedocs.org

* Sample code: Github_
    .. _Github: https://github.com/mtoshi/airwaveapiclient/blob/master/samples/sample.py

* Login ::

    >>> airwave = AirWaveAPIClient(username='admin',
    ...                            password='*****',
    ...                            url='https://192.168.1.1')
    >>> airwave.login()


* Get Access Point List ::

    >>> res = airwave.ap_list()
    >>> res.status_code
    200
    >>> res.text # xml output
    '<?xml version="1.0" encoding="utf-8" ...'


* Get Access Point Detail ::

    >>> ap_id = 1
    >>> res = airwave.ap_detail(ap_id)
    >>> res.status_code
    200
    >>> res.text # xml output
    '<?xml version="1.0" encoding="utf-8" ...'


* Logout ::

    >>> airwave.logout()


See also
========
* http://www.arubanetworks.com/products/networking/network-management/

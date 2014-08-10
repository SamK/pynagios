#!/usr/bin/env python
"""
= Module description:

This module is an attempt to calculate Nagios results from a Python script

= Notes:

This file tends to be PEP-8 compliant. Use these commands to be
proud of your work:

* using pep8:

  pep8 --ignore=E111 --ignore=E221  \
  --show-source --show-pep8 pynagios/pynagios.py

* using pyling:

  pylint --report=n --disable=R0902 pynagios/pynagios.py

= References:

* How to write Nagios plugins:
  http://nagiosplug.sourceforge.net/developer-guidelines.html

"""


class Perfdata:
    name = None
    value = None
    min_value = 0
    max_value = None
    warn_value = None
    crit_value = None


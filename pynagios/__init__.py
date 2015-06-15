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

from check import Check
from service import Service
from perfdata import Perfdata

__author__ = "Samuel Krieg"
__email__ = "samuel.krieg+github@gmail.com"
__version__ = "0.11"
__status__ = "Prod"


class NagiosError(Exception):
    """ Defines a custom error.
        This class just inherits from the standard Exception
        and does nothing more but changing the name.
    """
    pass


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

* How to create the documentation:

  pydoc -w  pynagios.pynagios

= References:

* How to write Nagios plugins:
  http://nagiosplug.sourceforge.net/developer-guidelines.html

"""

import sys

__author__ = "Samuel Krieg"
__email__ = "samuel.krieg+github@gmail.com"
__version__ = "0.11"
__status__ = "Dev"


class NagiosError(Exception):
    """ Defines a custom error.
        This class just inherits from the standard Exceptio
    """
    pass


class Service:
    """This is the nagios service. Each service has one value and one status"""

    label = None
    _value = None
    _status = None
    _text = None

    _perfdata_label = None
    _perfdata_min_level = 0
    _max_level = None
    _warn_level = None
    _crit_level = None
    _text = "%(label)s is %(status)s %(value)s/%(max_level)s"
    _perfdata = None

    def __init__(self, label):
        """ Create a Nagios service

            Keyword arguments:
            label      -- The label of the service
            value      -- The value returned by the sensor (default: None)
            warn_level -- The warning level (default: None)
            crit_level -- The critical level (default: None)
            max_level  -- the maximum level (default: None)
        """

        # apply variable given by user
        self.set_label(label)

    def __str__(self):
        output = ''
        variables = ['label', '_value', '_status', '_text',
                     '_perfdata_min_level', '_max_level', '_perfdata_label',
                     '_warn_level', '_crit_level',
                     '_perfdata']
        for varname in variables:
            value = getattr(self, varname)
            output += varname + " = " + str(value) + "\n"
        return output

    def perfdata(self, min_level=0, label=None):
        """ enable perfdata

            Keyword arguments:
            min_level  -- the minimum value of the service (default: 0)
            label      -- the service label (default: service label)
        """
        if label is None:
            self._perfdata_label = self.label
        else:
            self._perfdata_label = label

        self._perfdata_min_level = min_level

    def get_perfdata(self):
        """ returns the perfdata output
            the service data must be commited before using it
        """
        return self._perfdata

    def _dictvars(self):
        """ Returns a dictionnary of useful values
        """
        return {'label': self.get_label(),
                'status': self._status,
                'value': self._value,
                'max_level': self._max_level,
                'crit_level': self._crit_level,
                'warn_level': self._warn_level
               }

    def format_text(self, text):
        """Formats a text for Nagios output
        """
        try:
            return(text % self._dictvars())
        except KeyError as err:
            print "Some keys are not existing in the dictionnary: \"%s\""  % \
                   (err.args)
            raise

    def set_value(self, value):
        """Set the value of the service"""
        self._value = value

    def set_min_level(self, value):
        """set the minimum value of the service"""
        self._perfdata_min_level = value

    def set_max_level(self, value):
        """set the maximum value of the service"""
        self._max_level = value

    def set_warn_level(self, value):
        """set the warning level of the service"""
        self._warn_level = value

    def set_crit_level(self, value):
        """set the critical value of the service"""
        self._crit_level = value

    def set_text(self, text):
        """set the output text of the service"""
        self._text = text

    def get_text(self):
        """get the output text of the service"""
        return self._text

    def get_status(self):
        """get the Nagios status of the service"""
        return self._status

    def get_label(self):
        """get the label of the service"""
        return self.label

    def set_label(self, label):
        """set the label of the service"""
        self.label = label

    def _calc_status(self):
        """ determines the Nagios status of the service.
            the value can be gathered with get_status()
        """
        if isinstance(self._crit_level, basestring):
            if (self._crit_level[-1] == '%' and self._warn_level[-1] == '%'):
                #transformer les pourcentages en valeurs absolues
                self._crit_level = int(self._crit_level[:-1])
                self._warn_level = int(self._warn_level[:-1])
                self._warn_level = self._warn_level * self._max_level / 100
                self._crit_level = self._crit_level * self._max_level / 100
            elif (self._crit_level[-1] != '%' and self._warn_level[-1] != '%'):
                #pas un pourcentage mais quand meme transformer en int
                self._crit_level = int(self._crit_level)
                self._warn_level = int(self._warn_level)
            else:
                raise NagiosError("Cannot mix percentages and absolute values")

        if self._value >= self._crit_level:
            self._status = 'CRITICAL'
        elif self._value >= self._warn_level:
            self._status = 'WARNING'
        elif self._value is None:
            self._status = 'UNKNOWN'
        else:
            self._status = 'OK'

    def _calc_perfdata(self):
        """calculate perfdata"""
        value = self._value
        label = self._perfdata_label
        min_level = self._perfdata_min_level
        max_level = self._max_level
        warn_level = self._warn_level
        crit_level = self._crit_level
        #Return the perfdata string of an item
        self._perfdata = (
            "'%(label)s'=%(value).2f;"
            "%(warn_level)s;"
            "%(crit_level)s;"
            "%(min_level)s;"
            "%(max_level)s" % \
            {
            'label': label,
            'value': value,
            'warn_level': warn_level,
            'crit_level': crit_level,
            'min_level': min_level,
            'max_level': max_level
            }
        )

    def commit(self):
        """ Calculate the exit code and message of the service
            if perfdata, calculate perfdata
        """
        self._calc_status()
        if self._perfdata_label:
            self._calc_perfdata()


class Nagios:
    """This is the Nagios() class.
    """

    status_codes = {'OK': 0, 'WARNING': 1, 'CRITICAL': 2, 'UNKNOWN': 3}

    #The list of the services appened to this Nagios instance
    _services = []

    #The final perfdata string
    perfdata = ''

    text = ''
    label = ''

    def __init__(self):
        """The same status sorted from worst to best"""
        self.status_order = ['CRITICAL', 'WARNING', 'UNKNOWN', 'OK']
        self.status = None

    def _status_worst(self, status1, status2):
        """Compares two Nagios statuses and returns the worst"""
        for status in self.status_order:
            if status1 == status or status2 == status:
                return status

    def _status_best(self, status1, status2):
        """Compares two Nagios statuses and returns the best
           Just use the self._status_worst() method and return the opposite
        """
        worst = self._status_worst(status1, status2)
        if status1 == worst:
            return status2
        return status1

    def _status_lt(self, status1, status2):
        """Return true if status1 is lesser than status2
        """
        if status1 == status2:
            return False
        for status in self.status_order:
            if status1 == status:
                return True
            if status2 == status:
                return False
        raise Exception("Je fais quoi ici en comparant lt(%s, %s) ?" % \
                        (status1, status2))

    def _status_gt(self, status1, status2):
        """Returns true if status1 is greater than status2
        """
        if status1 == status2:
            return False
        for status in self.status_order:
            # if status2 is found, return true
            # if status1 is found, return false
            # if nothing is found, iterate
            if status == status2:
                return True
            if status == status1:
                return False
        raise Exception("Je fais quoi ici en comparant gt(%s, %s) ?" % \
                        (status1, status2))

    def exit_code(self, status=None):
        """Returns the exit code based on the status"""
        if status is None:
            raise Exception("No Nagios Status given")
        return self.status_codes[status]

    def exit(self):
        """Exit the script with the accurate Nagios status
        """
        sys.exit(self.exit_code(self.status))

    def add(self, service):
        """Adds a service into the Nagios instance.
           It automatically calculates the exit status
        """
        service.commit()
        self._services.append(service)
        if self.status is None:
            self.status = service.get_status()
            self.label = service.get_label()
            self.text = service.format_text(service.get_text())
        elif self._status_lt(service.get_status(), self.status):
            self.status = service.get_status()
            self.label = service.get_label()
            self.text = service.format_text(service.get_text())

        if service.get_perfdata():
            self.perfdata += ' ' + service.get_perfdata()

    def output(self):
        """Prints the final result
        """
        if not self._services:
            #raise Exception("wtf")
            raise NagiosError("No service defined")
        output = self.status + " - " + self.text
        if self.perfdata:
            output += ' |' + self.perfdata
        return output

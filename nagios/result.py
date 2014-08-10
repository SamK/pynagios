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

class Result:
    """ Will calculate and print the result
    """

    # the status codes
    status_codes = {'OK': 0, 'WARNING': 1, 'CRITICAL': 2, 'UNKNOWN': 3}
    # The same status sorted from worst to best
    status_order = ['CRITICAL', 'WARNING', 'UNKNOWN', 'OK']

    #The list of the services appened to this Results instance
    services = []

    name = None
    text = None
    status = None

    def __init__(self):
        pass

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

    def add(self, service):
        """Adds a service into the Result instance.
           It automatically calculates the exit status
        """
        service.commit()
        self.services.append(service)
        if self.status is None:
            self.status = service.status
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
        if not self.services:
            #raise Exception("wtf")
            raise NagiosError("No service defined")
        output = self.status + " - " + self.text
        if self.perfdata:
            output += ' |' + self.perfdata
        return output

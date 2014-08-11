#!/usr/bin/env python

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

    def print(self):
        """Prints the final result
        """
        output = self.status + " - " + self.text
        if self.perfdata:
            output += ' |' + self.perfdata
        return output

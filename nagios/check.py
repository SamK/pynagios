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
    exit_code = None

    def __init__(self):
        pass



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


    def exit(self):
        """Exit the script with the accurate Nagios status
        """
        sys.exit(self._exit_code(self.status))

    def add(self, service):
        """Adds a service into the Result instance and
           sets new result status and text
           It automatically calculates the exit status
        """
        # commit service
        service.commit()
        # Get new result status
        if self.status is None or  self._status_lt(service.status, self.status):
            # status and text are not exisitng. Must create
            self.status = service.status
            self.text = service.format_text(service.text)
            self.exit_code = self.status_codes[self.status]

        self.services.append(service)

    def output(self):
        """Prints the final result
        """
        if not self.services:
            raise NagiosError("No service defined")
        output = self.status + " - " + self.text
        #if self.perfdata:
        #    output += ' |' + self.perfdata
        return output

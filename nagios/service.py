#!/usr/bin/env python

class Service:
    """This is the nagios service. Each service has one value and one status.
       it can have multiple perfdata values
    """

    name = None
    value = None
    status = None

    max_level = None
    warn_level = None
    crit_level = None
    text = "%(name)s is %(status)s %(value)s/%(max_level)s"

    def __init__(self, name):
        """ Create a Nagios service
            a
            Keyword arguments:
            name       -- The label of the service
            value      -- The value returned by the sensor (default: None)
            warn_level -- The warning level (default: None)
            crit_level -- The critical level (default: None)
        """

        # apply variable given by user
        self.name = name

    def format_text(self, text):
        """Formats a text for Nagios output
        """
        try:
            dictvars = {'name': self.name,
                        'value': self.value,
                        'status': self.status,
                        'max_level': self.max_level,
                        'crit_level': self.crit_level,
                        'warn_level': self.warn_level}
            return(text % dictvars)
        except KeyError as err:
            print "Some keys are not existing in the dictionnary: \"%s\""  % \
                   (err.args)
            raise


    #
    # calculation methods
    #

    def set_status(self):
        """ set the Nagios status of the service.
        """

        absolute_crit_level = self.crit_level
        absolute_warn_level = self.warn_level
        if isinstance(self.crit_level, basestring):
            if (self.crit_level[-1] == '%' and self.warn_level[-1] == '%'):
                #transformer les pourcentages en valeurs absolues
                absolute_crit_level = int(self.crit_level[:-1])
                absolute_warn_level = int(self.warn_level[:-1])
                aboslute_crit_level = absolute_crit_level * self.max_level / 100
                absolute_warn_level = absolute_warn_level * self.max_level / 100
            elif (self.crit_level[-1] != '%' and self.warn_level[-1] != '%'):
                #pas un pourcentage mais quand meme transformer en int
                absolute_crit_level = int(self.crit_level)
                absolute_warn_level = int(self.warn_level)
            else:
                raise NagiosError("Cannot mix percentages and absolute values")

        if self.value is None:
            self.status = 'UNKNOWN'
        elif self.value >= absolute_crit_level:
            self.status = 'CRITICAL'
        elif self.value >= absolute_warn_level:
            self.status = 'WARNING'
        else:
            self.status = 'OK'


    def commit(self):
        """ Calculate the exit code and message of the service
            if perfdata, calculate perfdata
        """
        self.set_status()
        #self._calc_perfdata()


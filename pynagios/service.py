#!/usr/bin/env python

class Service:
    """This is the nagios service. Each service has one value and one status.
       it can have multiple perfdata values
    """

    name = None
    value = None
    status = None
    stringvalues = False

    ok_level = None
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

    def set_status_from_string_values(self):
        if self.value == self.ok_level:
            self.status = 'OK'
        elif self.value == self.warn_level:
            self.status = 'WARNING'
        elif self.value == self.crit_level:
            self.status = 'CRITICAL'
        elif self.crit_level is None:
            self.status = 'CRITICAL'
        elif self.warn_level is None:
            self.status = 'WARNING'
        elif self.ok_level is None:
            self.status = 'OK'
        else:
            self.status = 'UNKNOWN'


    def set_status_from_absolute_values(self, warn_level = None, crit_level = None):
        # get default values if not specified
        if warn_level is None:
            warn_level = self.warn_level
        if crit_level is None:
            crit_level = self.crit_level
        # set status based on value, warn and crit levels
        if self.value is None:
            self.status = 'UNKNOWN'
        elif self.value >= crit_level:
            self.status = 'CRITICAL'
        elif self.value >= warn_level:
            self.status = 'WARNING'
        else:
            self.status = 'OK'

    def get_absolute_values_from_percents(self):
        absolute_crit_level = int(self.crit_level[:-1])
        absolute_warn_level = int(self.warn_level[:-1])
        aboslute_crit_level = absolute_crit_level * self.max_level / 100
        absolute_warn_level = absolute_warn_level * self.max_level / 100
        return (absolute_warn_level, absolute_crit_level)

    def get_absolute_values_from_numeric(self):
        return (int(self.warn_level), int(self.crit_level))

    def get_absolute_values(self):
        if isinstance(self.crit_level, basestring):
            if (self.crit_level.endswith('%') and self.warn_level.endswith('%')):
                # we are dealing with percents
                warn_level, crit_level = self.get_absolute_values_from_percents()
            elif (not self.crit_level.endswith('%') and not self._warn_level.endswith('%')):
                warn_level, crit_level = self.get_absolute_values_from_numeric()
            else:
                raise NagiosError("Cannot mix percentages and absolute values")
        else:
             warn_level = self.warn_level
             crit_level = self.crit_level
        return (warn_level, crit_level)

    def set_status(self):
        if self.stringvalues:
            self.set_status_from_string_values()
        else:
            warn_level, crit_level = self.get_absolute_values()
            self.set_status_from_absolute_values(warn_level, crit_level)

    def commit(self):
        """ Calculate the exit code and message of the service
            if perfdata, calculate perfdata
        """
        self.set_status()
        #self._calc_perfdata()


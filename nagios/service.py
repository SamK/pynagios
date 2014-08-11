#!/usr/bin/env python

class Service:
    """This is the nagios service. Each service has one value and one status.
       it can have multiple perfdata values
    """

    name = None
    _value = None
    _status = None
    _text = None

    max_level = None
    warn_level = None
    crit_level = None
    _text = "%(name)s is %(status)s %(value)s/%(max_level)s"

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




    #def format_text(self, text):
        """Formats a text for Nagios output
        """
        """
        try:
            dictvars = {'name': self.name,
                        'status': self._status,
                        'value': self._value,
                        'max_level': self._max_level,
                        'crit_level': self._crit_level,
                        'warn_level': self._warn_level}
            return(text % self.dictvars)
        except KeyError as err:
            print "Some keys are not existing in the dictionnary: \"%s\""  % \
                   (err.args)
            raise
        """


    #
    # calculation methods
    #

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


    def commit(self):
        """ Calculate the exit code and message of the service
            if perfdata, calculate perfdata
        """
        self._calc_status()
        self._calc_perfdata()


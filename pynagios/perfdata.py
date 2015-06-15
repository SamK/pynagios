#!/usr/bin/env python


class Perfdata:
    label = None
    value = None
    min_level = 0
    max_level = None
    warn_level = None
    crit_level = None

    def __init__(self):
        pass

    def output(self):
        return "'%(label)s'=%(value)s;" \
                 "%(warn_level)s;" \
                 "%(crit_level)s;" \
                 "%(min_level)s;" \
                 "%(max_level)s" % \
                 {'label': self.label,
                  'value': self.value,
                  'warn_level': self.warn_level,
                  'crit_level': self.crit_level,
                  'min_level': self.min_level,
                  'max_level': self.max_level}

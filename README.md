pyNagios
========

This is a small Python library that I wrote for faster Nagios result analysing.

Note that I'm pretty sure that this script won't fit your needs.


Prerequisites
-------------

* Python 2.x

Installation
------------

* Linux:
    ./setup.py install

* Windows:
I have no idea

Usage
-----

import the module:
    from pynagios import pynagios

First step you should create one or more services and apply a few properties:
* name
* current value
* warning value
* critical value
* maximum value

The value can be integers (1, 2, 3), floats (3.14, 13.37), or strings.

The warning and critical levels can be string with percentage: ('13', '25%').
The library will autmatically convert the percentage into the absolute values.
However you cannot mix percentage and absolute values.

Example 1:
    service1 = pynagios.Service("Service1", 230, 850, 950, 1000)

Example 2:
    service2 = pynagios.service("Service2")
    service2.set_value(75)
    service2.set_max_level(100)
    service2.set_crit_level('75%')
    service2.set_warn_level('85%')
    # this one has perfdata:
    service2.perfdata()

Then you have to create a Nagios instance:

    nagios = pynagios.Nagios()

Finally, add the Services into the Nagios instance.

    nagios.add(service1)
    nagios.add(service2)

Time for some output:

    print nagios.output()

Time for exit with the good exit code:

    nagios.exit()

The end

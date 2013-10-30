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

The basics steps are:

1. import the module
2. create one pynagios.Nagios() instance
3. create one or more pynagios.Service() instances
4. Add pynagios.Service() into the pynagios.Nagios() instance
5. print the result
6. exit


Example:

    # 1. import the module
    from pynagios import pynagios

    # 2. create a nagios instance
    nagios = pynagios.Nagios()

    # 3. create your service
    my_service = pynagios.Service("Service1", 230, 850, 950, 1000)

    # 4. add your service into the nagios instance
    nagios.add(my_service)

    # 5. print the result
    print nagios.output()

    # 6. exit with the appropriate
    nagios.exit()

Example 2:

    # 1. import the module
    from pynagios import pynagios

    # 2. create a nagios instance
    nagios = pynagios.Nagios()

    # 3. create the first service
    service1 = pynagios.Service("Service1", 230, 850, 950, 1000)

    # 3b. create the second service
    service2 = pynagios.service("Service2")
    service2.set_value(75)
    service2.set_max_level(100)
    service2.set_crit_level('75%')
    service2.set_warn_level('85%')

    # 3c. enable perfdata
    service2.perfdata()

    # 4. add the services into the nagios instance
    nagios.add(service1)
    nagios.add(service2)

    # 5. print the result
    print nagios.output()

    # 6. exit with the appropriate
    nagios.exit()

The pynagios.Service() class accepts these arguments:
* name
* current value
* warning value
* critical value
* maximum value

The service value can be integers (1, 2, 3), floats (3.14, 13.37), or strings.

The warning and critical levels can be string with percentage: ('13', '25%').
The library will autmatically convert the percentage into the absolute values.
However you cannot mix percentage and absolute values.


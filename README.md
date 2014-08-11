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
2. create one or more pynagios.Service() instances
3. create one pynagios.Result() instance
4. Add pynagios.Service() into the pynagios.Result() instance
5. print the result
6. exit

Example 1: Simple result

```python
# 1. import the module
import nagios

# 2a. create the first service
service1 = nagios.Service("Service1")
service1.value(23)
service1.max_level(100)
service1.warn_level(85)
service1.crit_level(95)

# 3. create a "Result" instance
result = nagios.Result()

# 5. add the services into the nagios instance
result.add(service1)

# 5. print the result
result.print()

# 6. exit with the appropriate exit code
sys.exit(result.exit_code)

```

The service value can be integers (1, 2, 3) or floats (3.14, 13.37). No string yet.

The warning and critical levels can be string with percentage: ('13', '25%').
The library will autmatically convert the percentage into the absolute values.
However you cannot mix percentage and absolute values.

For more informations, maybe execute one of these commands: 

    pydoc pynagios.pynagios.Result
    pynagios.pynagios.Service

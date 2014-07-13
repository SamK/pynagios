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

Example:

```python
# 1. import the module
from pynagios import pynagios

# 2a. create the first service
service1 = pynagios.Service("Service1")
service1.set_value(230)
service1.set_max_level(100)
service1.set_warn_level(850)
service1.set_crit_level(950)

# 2b. create the second service
service2 = pynagios.Service("Service2")
service2.set_value(75)
service2.set_max_level(100)
service2.set_warn_level('85%')
service2.set_crit_level('95%')
# 2c. If needed, enable perfdata
service2.perfdata()

# 3. create a "result" instance
result = pynagios.Result()

# 5. add the services into the nagios instance
result.add(service1)
result.add(service2)

# 5. print the result
print result.output()

# 6. exit with the appropriate exit code
result.exit()
```

The service value can be integers (1, 2, 3), floats (3.14, 13.37), or strings.

The warning and critical levels can be string with percentage: ('13', '25%').
The library will autmatically convert the percentage into the absolute values.
However you cannot mix percentage and absolute values.

For more informations, maybe execute this command: 

    pydoc pynagios.pynagios.Result pynagios.pynagios.Service

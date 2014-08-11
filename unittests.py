#!/usr/bin/env python

import unittest
import sys


import nagios


class ReadmeExamples(unittest.TestCase):

    def test_example1

        # 2a. create the first service
        service1 = nagios.Service("Service1")
        service1.value(230)
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



class SimpleServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.result = nagios.Result()
        self.service = nagios.Service('single_service')
        self.service.max_level = 100


class Test_Exceptions(SimpleServiceTestCase):

    def test_no_service(self):
        with self.assertRaises(Exception):
            self.result.output()

    def test_no_value(self):
        self.service.value = None
        with self.assertRaises(Exception):
            self.result.add(self.service)
            self.result.output()

    def test_mix_abs_percent(self):
        self.service.warn_level = '80'
        self.service.crit_level = '90%'
        with self.assertRaises(Exception):
            self.result.add(self.service)

    def test_mix_percent_abs(self):
        self.service = warn_level = '50%'
        self.service = crit_level = '60'
        with self.assertRaises(Exception):
            self.result.add(self.service)


class Absolute_Values_TestCase(SimpleServiceTestCase):

    def setUp(self):
        super(Absolute_Values_TestCase, self).setUp()
        self.service.warn_level = 80
        self.service.crit_level = 90

    def test_result_ok(self):
        self.service.value = 1
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'OK')

    def test_result_warning(self):
        self.service.value = 81
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'WARNING')

    def test_result_critical(self):
        self.service.value = 91
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'CRITICAL')


class Percent_Values_TestCase(SimpleServiceTestCase):

    def setUp(self):
        super(Percent_Values_TestCase, self).setUp()
        self.service.warn_level = '80%'
        self.service.crit_level = '90%'

    def test_result_ok(self):
        self.service.value = 1
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'OK')

    def test_result_warning(self):
        self.service.value = 85
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'WARNING')

    def test_result_critical(self):
        self.service.value = 95
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'CRITICAL')


class No_Max_Value_TestCase(unittest.TestCase):
    def setUp(self):
        self.result = nagios.Result()
        self.service = nagios.Service('no_max_value')
        self.service.warn_level = 80
        self.service.crit_level = 90

    def test_result_ok(self):
        self.service.value = 10
        self.service.text = '%(label)s has value of %(value)s'
        self.result.add(self.service)
        print self.result
        self.assertEqual(self.result.status, 'OK')

    def test_result_warning(self):
        self.service.value = 81
        self.service.text = '%(label)s has value of %(value)s'
        self.result.add(self.service)
        print self.result
        self.assertEqual(self.result.status, 'WARNING')

    def test_result_critical(self):
        self.service.value = 91
        self.service.text = '%(label)s has value of %(value)s'
        self.result.add(self.service)
        print self.result
        self.assertEqual(self.result.status, 'CRITICAL')

class Exit_Code_TestCase(SimpleServiceTestCase):

    def test_exit_codes(self):
        self.assertEqual(self.result.exit_code('OK'), 0)
        self.assertEqual(self.result.exit_code('WARNING'), 1)
        self.assertEqual(self.result.exit_code('CRITICAL'), 2)
        self.assertEqual(self.result.exit_code('UNKNOWN'), 3)
        with self.assertRaises(Exception):
            self.result.exit_code()
            self.result.exit_code('a non existing status')


if __name__ == "__main__":
    unittest.main(verbosity=2)

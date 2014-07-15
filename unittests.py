#!/usr/bin/env python

import unittest
import sys


from pynagios import pynagios


class SimpleServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.result = pynagios.Result()
        self.service = pynagios.Service('single_service')
        self.service.set_max_level(100)


class Test_Exceptions(SimpleServiceTestCase):

    def test_no_service(self):
        with self.assertRaises(Exception):
            self.result.output()

    def test_no_value(self):
        self.service.set_value(None)
        with self.assertRaises(Exception):
            self.result.add(self.service)
            self.result.output()

    def test_mix_abs_percent(self):
        self.service.set_warn_level('80')
        self.service.set_crit_level('90%')
        with self.assertRaises(Exception):
            self.result.add(self.service)

    def test_mix_percent_abs(self):
        self.service.set_warn_level('50%')
        self.service.set_crit_level('60')
        with self.assertRaises(Exception):
            self.result.add(self.service)


class Absolute_Values_TestCase(SimpleServiceTestCase):

    def setUp(self):
        super(Absolute_Values_TestCase, self).setUp()
        self.service.set_warn_level(80)
        self.service.set_crit_level(90)

    def test_result_ok(self):
        self.service.set_value(1)
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'OK')

    def test_result_warning(self):
        self.service.set_value(81)
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'WARNING')

    def test_result_critical(self):
        self.service.set_value(91)
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'CRITICAL')


class Percent_Values_TestCase(SimpleServiceTestCase):


    def setUp(self):
        super(Percent_Values_TestCase, self).setUp()
        self.service.set_warn_level('80%')
        self.service.set_crit_level('90%')

    def test_result_ok(self):
        self.service.set_value(1)
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'OK')

    def test_result_warning(self):
        self.service.set_value(85)
        self.result.add(self.service)
        self.assertEqual(self.result.status, 'WARNING')

    def test_result_critical(self):
        self.service.set_value(95)
        self.result.add(self.service)
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

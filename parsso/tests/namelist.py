#!/usr/bin/env python3

import unittest
from collections import OrderedDict

from parsso.namelist.basic import *

data = OrderedDict({
    'calculation': 'scf',
    'verbosity': ('low', 'CONTROL'),
    'dt': 20,
    'ibrav': 0,
    'celldm(0)': 1
})

variables = []
for k, v in data.items():
    if type(v) is tuple:
        variables.append(NamelistVariable(k, *v))
    else:
        variables.append(NamelistVariable(k, v))


class TestNamelistVariable(unittest.TestCase):
    def test_value_types(self):
        types = (str, str, float, int, list)
        for _, t in zip(variables, types):
            self.assertTrue(type(_.value) is t)

    def test_in_namelists(self):
        namelists = ('CONTROL', 'CONTROL', 'CONTROL', 'SYSTEM', 'SYSTEM')
        for _, n in zip(variables, namelists):
            self.assertTrue(_.in_namelist == n)


class TestNamelist(unittest.TestCase):
    def setUp(self):
        self.control_namelist = Namelist({
            'calculation': NamelistVariable('calculation', 'scf'),
            'verbosity': NamelistVariable('verbosity', 'low', 'CONTROL'),
            'dt': NamelistVariable('dt', 20)
        })

    def test_type_error(self):
        self.assertRaises(TypeError, Namelist, variables)

    def test_in_same_namelist(self):
        names = (_.name for _ in variables)
        self.assertRaises(ValueError, Namelist, dict(zip(names, variables)))

    def test_namelist(self):
        for _ in self.control_namelist.values():
            self.assertTrue(_.in_namelist, 'CONTROL')

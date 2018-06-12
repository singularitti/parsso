#!/usr/bin/env python3


import re
from typing import Optional, List

import addict
import lazy_property

from parsso.namelist.default import all_names, all_namelists

# ========================================= What can be exported? =========================================
__all__ = ['NamelistVariable', 'Namelist']


class NamelistVariable(object):
    def __init__(self, name, value, in_namelist: Optional[str] = None):
        # Type checking.
        if not isinstance(name, str):
            raise TypeError("Argument *name* must be a string!")

        if not isinstance(value, (int, float, bool, str, list)):
            raise TypeError("Argument *value* is of wrong type '{0}'!".format(type(value).__name__))

        if in_namelist and not isinstance(in_namelist, str):
            raise TypeError("Argument *in_namelist* must be a string!")

        name = name.lower()  # In case that user inputs wrong case.

        self.__index = None
        if '(' in name:  # If user inputs a name containing '(i)'.
            # Only take the part before the first '('
            match = re.match("(\w+)\(?(\d*)\)?", name)
            if match is None:
                raise ValueError("Invalid index in *name*!")
            name, index = match.groups()
            self.__index = int(index)

        in_which_namelist = all_names()[name]  # Find where does the name locates.
        if len(in_which_namelist) == 0:
            raise KeyError("Name '{0}' not found!".format(name))
        elif len(in_which_namelist) > 1:
            if in_which_namelist is None:
                raise ValueError("Name '{0}' appears in multiple namelists, try explicitly specify it!".format(name))

            if in_namelist.upper() not in {'CONTROL', 'SYSTEM', 'ELECTRONS', 'IONS', 'CELL', 'INPUTPH'}:
                raise ValueError('Unrecognized argument *in_namelist*!')
        self.__in_namelist = in_which_namelist.pop()

        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self):
        if self.default_type == List[float]:
            return [float(self.__value) if i == self.index else None for i in range(6)]

        return self.default_type(self.__value)

    @value.setter
    def value(self, new_value) -> None:
        if not isinstance(new_value, (int, float, bool, str, list)):
            raise TypeError("Argument *value* is of wrong type '{0}'!".format(type(new_value).__name__))

        self.__value = new_value

    @lazy_property.LazyProperty
    def default_type(self) -> str:
        return all_namelists()[self.__in_namelist][self.__name]

    @property
    def in_namelist(self) -> str:
        return self.__in_namelist

    @property
    def index(self) -> int:
        return self.__index

    def __eq__(self, other: object) -> bool:
        if not type(other) is NamelistVariable:
            return False

        attributes = ['name', 'default_type', 'value', 'in_namelist']
        return all(getattr(self, attr) == getattr(other, attr) for attr in attributes)

    def __ne__(self, other: object) -> bool:
        if not type(other) is NamelistVariable:
            return False

        attributes = ['name', 'default_type', 'value', 'in_namelist']
        return any(getattr(self, attr) != getattr(other, attr) for attr in attributes)


class Namelist(addict.Dict):
    def __init__(self, d):
        if not isinstance(d, dict):
            raise TypeError("Argument *d* must be a dictionary!")

        if not all(type(v) is NamelistVariable for v in d.values()):
            raise TypeError("All values in *d* must be of type 'NamelistVariable'!")

        benchmark = next(iter(d.values())).in_namelist
        if not all(v.in_namelist == benchmark for v in d.values()):
            raise ValueError("All values must be in the same namelist!")

        self.__name = benchmark

        super().__init__(d)

    @property
    def name(self) -> str:
        return self.__name

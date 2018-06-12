#!/usr/bin/env python3

import addict

# ========================================= What can be exported? =========================================
__all__ = ['Card']


class Card(addict.Dict):
    def __init__(self, d):
        if not isinstance(d, dict):
            raise TypeError

        if set(d.keys()) <= {'values', 'option'}:
            raise KeyError

        self.__data = d['values']
        self.__option = d['option']

        super().__init__(d)

    @property
    def data(self):
        return self.__data

    @property
    def option(self):
        return self.__option


class AtomicSpecies(Card):
    def species(self):
        return (_[0] for _ in self.data)

    def masses(self):
        return (_[1] for _ in self.data)

    def pseudopotentials(self):
        return (_[2] for _ in self.data)


class AtomicPosition(Card):
    pass


class CellParameters(Card):
    pass

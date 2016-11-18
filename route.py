# -*- coding: utf-8 -*-
from itertools import combinations
from typing import List, Iterator

from flight import Flight

__all__ = ['Route']


class Route(object):
    """Class for holding information about route

    Todo:
        * Filip Vavera: class string representation
    """
    def __init__(self, first_flight: Flight) -> None:
        """Initialize with given values

        Arguments:
            first_flight: first flight of the route
        """
        self._route = [first_flight, ]
        self._current = 0

    def __iter__(self) -> Iterator['Route']:
        return self

    def __next__(self) -> Flight:
        if self._current == len(self._route) - 1:
            raise StopIteration
        else:
            self._current += 1
            return self._route[self._current - 1]

    def __repr__(self) -> str:
        return ''  # TODO (Filip Vavera)

    @property
    def flights(self) -> List[Flight]:
        """All flights in the route in order"""
        return self._route

    @property
    def price(self) -> int:
        """Price for the route"""
        result = 0
        for f in self._route:
            result += f.price
        return result

    @property
    def price_1bag(self) -> int:
        """Price for route with one bag"""
        if not self.is_1bag_route:
            raise Exception('This is not one bag route.')
        result = 0
        for f in self._route:
            result += f.price_1bag
        return result

    @property
    def price_2bag(self) -> int:
        """Price for route with two bags"""
        if not self.is_2bag_route:
            raise Exception('This is not two bag route.')
        result = 0
        for f in self._route:
            result += f.price_2bag
        return result

    @property
    def is_1bag_route(self) -> bool:
        """Can be absolved with one bag"""
        for f in self._route:
            if f.bags_allowed < 1:
                return False
        return True

    @property
    def is_2bag_route(self) -> bool:
        """Can be absolved with two bags"""
        for f in self._route:
            if f.bags_allowed < 2:
                return False
        return True

    @property
    def source(self) -> str:
        """Route source airport"""
        return self._route[0].source

    @property
    def destination(self) -> str:
        """Route destination airport"""
        return self._route[-1].destination

    @property
    def is_valid(self) -> bool:
        """Is route valid according conditions given in task description"""
        for pair in combinations(self._route, 2):
            if (pair[0].source == pair[1].source and
                    pair[0].destination == pair[1].destination):
                return False
        return True

    def add_flight(self, flight: Flight) -> None:
        """Add next flight to the route

        Arguments:
            flight: flight to add to the route

        Raises:
            Exception: when flight doesn't follow
        """
        if len(self._route) == 0 or flight in self._route[-1].follows:
            self._route.append(flight)
        else:
            raise Exception('Invalid route.')

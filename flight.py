# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import List

__all__ = ['Flight']


class Flight(object):
    """Class for holding information about flight"""
    date_format = '%Y-%m-%dT%H:%M:%S'
    """int: datetime string format"""

    def __init__(self, source: str, destination: str,
                 departure: datetime, arrival: datetime,
                 flight_number: str, price: int, bags_allowed: int,
                 bag_price: int) -> None:
        """Initialize with given values

        Arguments:
            source: flight source airport
            destination: flight destination airport
            departure: flight departure
            arrival: flight arrival
            flight_number: flight number
            price: flight price
            bags_allowed: number of allowed bags
            bag_price: price for one additional bag
        """
        self._source = source
        self._destination = destination
        self._departure = departure
        self._arrival = arrival
        self._flight_number = flight_number
        self._price = price
        self._bags_allowed = bags_allowed
        self._bag_price = bag_price
        self._follows = []

    def __repr__(self) -> str:
        return '{},{},{},{},{},{},{},{}'.format(
            self._source, self._destination,
            self._departure.strftime(self.date_format),
            self._arrival.strftime(self.date_format), self._flight_number,
            self._price, self._bags_allowed, self._bag_price)

    @property
    def source(self) -> str:
        """Flight source"""
        return self._source

    @property
    def destination(self) -> str:
        """Flight destination"""
        return self._destination

    @property
    def departure(self) -> datetime:
        """Flight departure"""
        return self._departure

    @property
    def arrival(self) -> datetime:
        """Flight arrival"""
        return self._arrival

    @property
    def flight_number(self) -> str:
        """Flight number"""
        return self._flight_number

    @property
    def price(self) -> int:
        """Flight price"""
        return self._price

    @property
    def price_1bag(self) -> int:
        """Flight price with one bag"""
        if self._bags_allowed < 1:
            raise Exception('Bag is not allowed for this flight.')
        return self._price + self._bag_price

    @property
    def price_2bag(self) -> int:
        """Flight price with two bags"""
        if self._bags_allowed < 1:
            raise Exception('Two bags are not allowed for this flight.')
        return self._price + 2 * self._bag_price

    @property
    def bags_allowed(self) -> int:
        """Number of allowed bags"""
        return self._bags_allowed

    @property
    def bag_price(self) -> int:
        """Price for one additional bag"""
        return self._bag_price

    @property
    def follows(self) -> List['Flight']:
        """Flights that follows"""
        return self._follows

    @property
    def follows_1bag(self) -> List['Flight']:
        """Flights that follows with at least one bag enabled"""
        return [f for f in self._follows if f.bags_allowed >= 1]

    @property
    def follows_2bag(self) -> List['Flight']:
        """Flights that follows with at least two bags enabled"""
        return [f for f in self._follows if f.bags_allowed >= 2]

    def add_follows(self, flights: List['Flight']) -> None:
        """Add flights that follows from all flights

        Arguments:
            flights: all flights where should be looking for flights that
                     follows
        """
        for flight in flights:
            if (flight.source == self.destination and
                    timedelta(hours=1) <= flight.departure - self.arrival <=
                    timedelta(hours=4)):
                self._follows.append(flight)

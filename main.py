#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from typing import List

from flight import Flight
from route import Route


def parse(line: str) -> Flight:
    """Parse one input line to Flight class

    Arguments:
        line: One line form program input

    Returns:
        Flight instance
    """
    args = line.split(',')

    # Datetime
    date_format = Flight.date_format
    args[2] = datetime.strptime(args[2], date_format)
    args[3] = datetime.strptime(args[3], date_format)
    # Price
    args[5] = int(args[5])
    # Bags allowed
    args[6] = int(args[6])
    # Bag price
    args[7] = int(args[7])

    return Flight(*args)


def finish_route(routes: List[Route], index: int) -> None:
    """Complete flight route (recursive)

    Arguments:
        routes: List of all routes
        index: Index of the route that should be completed
    """
    route = routes[index]

    # if route cannot continue
    if len(route.flights[-1].follows) == 0:
        return

    # if there is more then one way how to continue
    if len(route.flights[-1].follows) > 1:
        for follow in route.flights[-1].follows[1:]:
            new = Route(route.flights[0])       # copy the instance would be
            for flight in route.flights[1:]:    # more intelligent but I wasn't
                new.add_flight(flight)          # able to get it work
            new.add_flight(follow)
            routes.append(new)

    # add next fly
    routes[index].add_flight(route.flights[-1].follows[0])
    # continue with completing this route
    finish_route(routes, index)


if __name__ == '__main__':
    inp = [i.rstrip('\n') for i in list(sys.stdin)]

    if inp[0] != ('source,destination,departure,arrival,flight_number,'
                  'price,bags_allowed,bag_price'):
        raise Exception('Unrecognized input.')

    flights = []
    # parse all input lines into Flight class
    for line in inp[1:]:
        # skip empty lines
        if not line.strip():
            continue
        flights.append(parse(line))

    # add next possible flights to all flights
    for flight in flights:
        flight.add_follows(flights)

    routes = []
    # create routes starting with flights which has follow flight
    for flight in flights:
        if len(flight.follows) == 0:
            continue
        routes.append(Route(flight))

    # finish all routes
    for i in range(len(routes)):
        finish_route(routes, i)

    # print no bag routes
    print('No bag:\n' + '-' * 80)
    for route in [r for r in routes if r.is_valid]:
        print('{} -> {}, price: {}'.format(route.source, route.destination,
                                           route.price))
        for flight in route.flights:
            print('\t{}'.format(flight))
        print()

    # print one bag routes
    print('One bag:\n' + '-' * 80)
    for route in [r for r in routes if r.is_valid and r.is_1bag_route]:
        print('{} -> {}, price: {}'.format(route.source, route.destination,
                                           route.price_1bag))
        for flight in route.flights:
            print('\t{}'.format(flight))
        print()

    # print two bag routes
    print('Two bags:\n' + '-' * 80)
    for route in [r for r in routes if r.is_valid and r.is_2bag_route]:
        print('{} -> {}, price: {}'.format(route.source, route.destination,
                                           route.price_2bag))
        for flight in route.flights:
            print('\t{}'.format(flight))
        print()

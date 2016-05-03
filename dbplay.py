import requests
from xml.etree import ElementTree
import os
from bart_info import gets_lat_lon_for_many_stops
from muni_info import gets_stop_lat_lon_routes

# from model import Agency, Route

TOKEN_511 = os.environ.get("TOKEN")

wanted_agencies = ("BART", "SF-MUNI", "Caltrain")


def gets_agencies():
    """gets all the available agencies with HasDirection"""

    list_of_agencies = 'http://services.my511.org/Transit2.0/GetAgencies.aspx?token=' + TOKEN_511

    response_agencies = requests.get(list_of_agencies)

    agencies_tree = ElementTree.fromstring(response_agencies.text)

    agencies = {}

    for node in agencies_tree.iter('Agency'):
        name = node.attrib.get('Name')
        if name in wanted_agencies:
            has_direction = node.attrib.get('HasDirection')
            agencies[name] = has_direction

            # agency = Agency(
            #             name=name,
            #             has_direction=has_direction,
            #             )

            # db.session.add(agency)

    # db.session.commit()

    return agencies


def gets_routes_for_agency(agencies):
    """gets the routes for an agency"""

    routes = {}

    for wanted_agency in agencies:
        agency = wanted_agency

        agency_routes = 'http://services.my511.org/Transit2.0/GetRoutesForAgency.aspx?token=' + TOKEN_511 + '&agencyName=' + agency

        response_agency_routes = requests.get(agency_routes)

        route_tree = ElementTree.fromstring(response_agency_routes.text)

        # print response_agency_routes.text


        for node in route_tree.iter('Route'):
            name = node.attrib.get('Name')
            code = node.attrib.get('Code')
            routes[name] = (code, agency, agencies[wanted_agency])

        #     route = Route(
        #                 route_id=int(code),
        #                 name=name,
        #                 agency_name=agency
        #                 )

        #     db.session.add(route)

        # db.session.commit()

    return routes


def gets_stops_for_a_route(url):
        response = requests.get(url)

        stops_tree = ElementTree.fromstring(response.text)

        stops = []

        for node in stops_tree.iter('Stop'):
            name = node.attrib.get('name')
            code = node.attrib.get('StopCode')
            stops.append((name, code))

        return stops

def gets_stops_for_routes(routes):
    """gets all the stops for a route"""

    new_routes = {}

    for route in routes:
#       '44-OShaughnessy': ('44', 'SF-MUNI', 'True')}
        route_code = routes[route][0]
        agency = routes[route][1]
        direction = routes[route][2]

        if agency == "SF-MUNI":
            for direction in ["Inbound", "Outbound"]:
                url = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN_511 + '&routeIDF=' + agency + '~' + route_code + '~' + direction
                stops = gets_stops_for_a_route(url)
                new_routes[route, direction] = {"route_code": route_code, "agency": agency, "direction": direction, "stops": stops}

        if agency == "Caltrain":
            for direction in ["NB", "SB1", "SB2", "SB3"]:
                url = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN_511 + '&routeIDF=' + agency + '~' + route_code + '~' + direction
                stops = gets_stops_for_a_route(url)
                new_routes[route, direction] = {"route_code": route_code, "agency": agency, "direction": direction, "stops": stops}

        elif agency == "BART":
            url = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN_511 + '&routeIDF=' + agency + '~' + route_code
            stops = gets_stops_for_a_route(url)
            new_routes[route, direction] = {"route_code": route_code, "agency": agency, "direction": direction, "stops": stops}

    return new_routes


def gets_departure_time_by_stop(stop):
    """gets all the departure times for a stop"""

    times_for_stops = 'http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx?token=' + TOKEN_511 + '&stopcode=' + stop

    response_times_for_stops = requests.get(times_for_stops)

    departure_tree = ElementTree.fromstring(response_times_for_stops.text)

    departures = {}

    for node in departure_tree.iter('Route'):
        name = node.attrib.get('Name')
        # code = node.attrib.get('Code')
        for n in node.iter('DepartureTime'):
            departures.setdefault(name, []).append(n.text)

    return departures


def get_stop_for_user_route(user_stop, destination_stop, agency, route, direction):
    """returns a list of stops for user's route"""

    stops = gets_stops_for_route(agency, route, direction)
    print "this is the orginal stops", stops
    for num in range(len(stops)):
        if user_stop == stops[num][1]:
            forward = True
            start = num
            break
        if destination_stop == stops[num][1]:
            forward = False
            start = 0
            break
    if not forward:
        stops.reverse()
    print "this is after reversed", stops
    route = []
    print "THIS IS FROM THE START", stops[start:]
    for stop in stops[start:]:
        print stop
        route.append(stop)
        if stop[1] == destination_stop:
            break

    return route


def checks_stop_names_same(stops_routes_agencies_info):
    s = {}
    for stop in stops_routes_agencies_info:
        for st in stops_routes_agencies_info[stop]["stops"]:
            s.setdefault(st[1], []).append(st[0])
    names_same = True
    # checks if the names match:
    for item in s:
        if len(s[item]) > 1:
            match = s[item][0]
            for i in s[item]:
                if i != match:
                    print "this is the thing", item
                    print "this is the thing's thing:", s[item]
                    names_same = False

    return names_same


def gets_just_stops_from_info(stops_routes_agencies_info):

    stops = {"SF-MUNI": set(), "BART": set(), "Caltrain": set()}

    for item in stops_routes_agencies_info:
        for stop in stops_routes_agencies_info[item]['stops']:
            agency = stops_routes_agencies_info[item]['agency']
            stops[agency].add(stop)

    return stops


def add_stops_to_db(stops_routes_agencies_info):
    """addes stop and their info to db"""

    for item in stops_routes_agencies_info:
        print "this is Route name:",item
        print "this is the direction:", stops_routes_agencies_info[item]['direction']
        print "this is the route_code:", stops_routes_agencies_info[item]['route_code']
        print "this is the agency:", stops_routes_agencies_info[item]['agency']
        print "these are the stops:", stops_routes_agencies_info[item]['stops']

        # route = Stop(
        #             route_id=int(code),
        #             name=name,
        #             agency_name=agency
        #             )

        #     db.session.add(route)

        # db.session.commit()

def gets_muni_routes(routes_agencies_info):
    """returns only the routes for muni"""

    muni = []
    for item in routes_agencies_info:
        if routes_agencies_info[item]['agency'] == "SF-MUNI":
            muni.append(item)

    return muni


agencies_info = gets_agencies()
routes_agencies_info = gets_routes_for_agency(agencies_info)
stops_routes_agencies_info = gets_stops_for_routes(routes_agencies_info)
# muni_stops = gets_stop_lat_lon_routes(gets_muni_routes(routes_agencies_info))
stops = gets_just_stops_from_info(stops_routes_agencies_info)
bart_stops_lat_lng = gets_lat_lon_for_many_stops(stops['BART'])







# if __name__ == "__main__":
#     connect_to_db(app)
#     db.create_all()

#     load_agencies()
#     load_routes()
#     load_stops()

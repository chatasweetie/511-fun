import requests
from xml.etree import ElementTree
import os

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


def gets_stops_for_route(routes):
    """gets all the stops for a route"""
    stops = []

    for route in routes:
#       '44-OShaughnessy': ('44', 'SF-MUNI', 'True')}
        print "this is the route:", route
        route_code = routes[route][0]
        agency = routes[route][1]
        direction = routes[route][2]
        print "this is the agency:", agency
        print "this is the direction:", direction

        if direction:
            print "GOT INTO IF"
            for direction in ["Inbound", "Outbound"]:
                list_of_stops_agency = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN_511 + '&routeIDF=' + agency + '~' + route_code + '~' + direction
                print list_of_stops_agency
        else:
            print "GOT INTO ELSE"
            list_of_stops_agency = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN_511 + '&routeIDF=' + agency + '~' + route_code
            print list_of_stops_agency
        response_list_of_stops = requests.get(list_of_stops_agency)

        stops_tree = ElementTree.fromstring(response_list_of_stops.text)

        for node in stops_tree.iter('Stop'):
            name = node.attrib.get('name')
            code = node.attrib.get('StopCode')
            stops.append((name, code))

            # stop = Stop(
            #             stop=code,
            #             name=name,
            #             )

            #     db.session.add(stop)

            # db.session.commit()

    return stops


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


agencies = gets_agencies()
routes = gets_routes_for_agency(agencies)
stops = gets_stops_for_route(routes)

# if __name__ == "__main__":
#     connect_to_db(app)
#     db.create_all()

#     load_agencies()
#     load_routes()
#     load_stops()

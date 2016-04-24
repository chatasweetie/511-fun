import requests
from xml.etree import ElementTree
import os

TOKEN = os.environ.get("TOKEN")


def gets_agencies(TOKEN):
    """gets all the available agencies with HasDirection"""

    list_of_agencies = 'http://services.my511.org/Transit2.0/GetAgencies.aspx?token=' + TOKEN

    response_agencies = requests.get(list_of_agencies)

    agencies_tree = ElementTree.fromstring(response_agencies.text)

    agencies = {}

    for node in agencies_tree.iter('Agency'):
        name = node.attrib.get('Name')
        has_direction = node.attrib.get('HasDirection')
        agencies[name] = has_direction

    return agencies


def gets_routes_for_agency(TOKEN, agency):
    """gets the routes for an agency"""

    response_agency_routes = requests.get(agency_routes)

    route_tree = ElementTree.fromstring(response_agency_routes.text)

    routes = {}

    for node in route_tree.iter('Route'):
        name = node.attrib.get('Name')
        code = node.attrib.get('Code')
        routes[name] = code

    return routes


def gets_stops_for_route(TOKEN, agency, route, route_direction=""):
    """gets all the stops for a route"""

    if route_direction == "":
        list_of_stops_agency = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN + '&routeIDF=' + agency + '~' + route
    else:
        list_of_stops_agency = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN + '&routeIDF=' + agency + '~' + route + '~' + route_direction

    response_list_of_stops = requests.get(list_of_stops_agency)

    stops_tree = ElementTree.fromstring(response_list_of_stops.text)

    stops = []

    for node in stops_tree.iter('Stop'):
        name = node.attrib.get('name')
        code = node.attrib.get('StopCode')
        stops.append((name, code))

    return stops


def gets_departure_time_by_stop(TOKEN, stop):
    """gets all the departure times for a stop"""

    times_for_stops = 'http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx?token=' + TOKEN + '&stopcode=' + stop

    response_times_for_stops = requests.get(times_for_stops)

    departure_tree = ElementTree.fromstring(response_times_for_stops.text)

    departures = {}

    for node in departure_tree.iter('Route'):
        name = node.attrib.get('Name')
        for n in node.iter('DepartureTime'):
            departures.setdefault(name, []).append(n.text)

    return departures

list_of_agencies = 'http://services.my511.org/Transit2.0/GetAgencies.aspx?token=' + TOKEN

agency = "BART"
agency_routes = 'http://services.my511.org/Transit2.0/GetRoutesForAgency.aspx?token=' + TOKEN + '&agencyName=' + agency

route = "917"
RouteDirectionCode = ""
list_of_stops_agency = 'http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=' + TOKEN + '&routeIDF=' + agency + '~' + route


stop = "11"
times_for_stops = 'http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx?token=' + TOKEN + '&stopcode=' + stop


r_agencies = requests.get(list_of_agencies)
print "this is the request", r_agencies

r_list_of_stops = requests.get(list_of_stops_agency)
print "this is the request", r_list_of_stops

response_agency_routes = requests.get(agency_routes)
print "this is the request", response_agency_routes

r_times_for_stops = requests.get(times_for_stops)
print "this is the request", r_times_for_stops

# gives a list of routes for an agency
route_tree = ElementTree.fromstring(response_agency_routes.text)

routes = {}

for node in route_tree.iter('Route'):
    name = node.attrib.get('Name')
    code = node.attrib.get('Code')
    routes[name] = code


# gets a list of agencies
agencies_tree = ElementTree.fromstring(r_agencies.text)

agencies = {}

for node in agencies_tree.iter('Agency'):
    name = node.attrib.get('Name')
    has_direction = node.attrib.get('HasDirection')
    agencies[name] = has_direction

# to get all the stops and stopcodes for a line
stops_tree = ElementTree.fromstring(r_list_of_stops.text)

stops = []

for node in stops_tree.iter('Stop'):
    name = node.attrib.get('name')
    code = node.attrib.get('StopCode')
    stops.append((name, code))


# to get by the line, the departure times
departure_tree = ElementTree.fromstring(r_times_for_stops.text)

departures = {}

for node in departure_tree.iter('Route'):
    name = node.attrib.get('Name')
    code = node.attrib.get('Code')
    for n in node.iter('DepartureTime'):
        departures.setdefault(name, []).append(n.text)

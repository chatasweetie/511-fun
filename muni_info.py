import requests
from xml.etree import ElementTree


muni_stops = ['8AX-Bayshore A Express', 'Parkmerced', '30X-Marina Express', '39-Coit', '18-46th Avenue', 'T-Owl', 'Treasure Island', '1BX-California B Express', '66-Quintara', '8BX-Bayshore B Express', 'Powell Hyde Cable Car', 'Mission Rapid', 'Powell Mason Cable Car', '27-Bryant', '91-Owl', '3-Jackson', '38BX-Geary B Express', '41-Union', 'NX-N Express', '6-Haight-Parnassus', 'L-Owl', 'K-Owl', '1-California', 'J-Church', 'M-Owl', '22-Fillmore', '19th Avenue Rapid', '33-Ashbury-18th', '55-16th Street', '88-Bart Shuttle', '81X-Caltrain Express', '14-Mission', '83X-Caltrain', '14X-Mission Express', '45-Union Stockton', '28-19th Avenue', 'San Bruno Rapid', 'Fulton Rapid', '31-Balboa', '49-Van Ness Mission', '23-Monterey', '67-Bernal Heights', '38-Geary', '82X-Levi Plaza Express', '10-Townsend', '56-Rutland', 'L-Taraval', '37-Corbett', '19-Polk', '38AX-Geary A Express', '43-Masonic', '1AX-California A Express', '90-San Bruno Owl', 'Geary Rapid', '29-Sunset', '36-Teresita', '54-Felton', '47-Van Ness', '5-Fulton', 'HaightNoriega Rapid', '31AX-Balboa A Express', 'M-Ocean View', '12-Folsom Pacific', '52-Excelsior', 'N-Judah', 'KT-Ingleside Third Street', '21-Hayes', 'HaightNoriega', '48-Quintara 24th Street', 'N-Owl', '8-Bayshore', '31BX-Balboa B Express', 'California Cable Car', 'Noriega Express', '76X-Marin Headlands Express', '35-Eureka', 'F-Market And Wharves', '24-Divisadero', '9-San Bruno', '30-Stockton', '2-Clement', '44-OShaughnessy']

routes = []

for route in muni_stops:
    i = route.split('-')
    if len(i) == 1:
        i[0].split(" ")
    routes.append(i)

route_stops = {}

for i in range(len(muni_stops)):

    route = routes[i]

    url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r=' + route[0]

    response_agencies = requests.get(url)

    agencies_tree = ElementTree.fromstring(response_agencies.text)

    for node in agencies_tree.iter('stop'):
        stop_id = node.attrib.get('tag')
        name = node.attrib.get('title')
        lat = node.attrib.get('lat')
        lon = node.attrib.get('lon')
        print "stop id:", stop_id
        print "name:", name
        print "lat:", lat
        print "lon:", lon
        if name is None:
            break
        route_stops[muni_stops[i]] = {'name': name, 'stop_id': stop_id, 'lat': lat, 'lon': lon}



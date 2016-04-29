import requests
from xml.etree import ElementTree
import os

BART_TOKEN = os.environ.get("BART_TOKEN")

stops = [('16th St. Mission (SF)', '10'), ('Civic Center (SF)', '12'), ('Powell St. (SF)', '14'), ('Montgomery St. (SF)', '16'), ('Embarcadero (SF)', '18'), ('West Oakland', '20'), ('Concord', '52'), ('Pleasant Hill/Contra Costa Centre', '54'), ('Walnut Creek', '56'), ('Lafayette', '58'), ('Orinda', '60'), ('Rockridge (Oakland)', '62'), ('MacArthur (Oakland)', '64'), ('19th St. Oakland', '66'), ('12th St. Oakland City Center', '68'), ('North Concord/Martinez', '70'), ('Colma', '72'), ('Pittsburg/Bay Point', '78'), ('South San Francisco', '80'), ('San Bruno', '82'), ("San Francisco Int'l Airport", '85'), ('Daly City', '92'), ('Balboa Park (SF)', '94'), ('Glen Park (SF)', '96'), ('24th St. Mission (SF)', '98')]

bart_station_abbr_name = {'Ashby (Berkeley)': 'ashb', 'Powell St. (SF)': 'powl', 'Coliseum': 'cols', 'San Leandro': 'sanl', 'North Concord/Martinez': 'ncon', 'Richmond': 'rich', 'Pleasant Hill': 'phil', '19th St. Oakland': '19th', 'Hayward': 'hayw', '12th St. Oakland City Center': '12th', 'Bay Fair (San Leandro)': 'bayf', 'Civic Center (SF)': 'civc', 'Castro Valley': 'cast', 'Fremont': 'frmt', 'Lake Merritt (Oakland)': 'lake', 'West Oakland': 'woak', '24th St. Mission (SF)': '24th', 'El Cerrito Plaza': 'plza', 'Millbrae': 'mlbr', 'Colma': 'colm', 'Downtown Berkeley': 'dbrk', 'Balboa Park (SF)': 'balb', 'Embarcadero (SF)': 'embr', 'El Cerrito del Norte': 'deln', 'Dublin/Pleasanton': 'dubl', 'Lafayette': 'lafy', "Oakland Int'l Airport": 'oakl', 'Fruitvale (Oakland)': 'ftvl', '16th St. Mission (SF)': '16th', 'Walnut Creek': 'wcrk', 'MacArthur (Oakland)': 'mcar', 'San Bruno': 'sbrn', 'Rockridge (Oakland)': 'rock', 'Daly City': 'daly', 'Concord': 'conc', 'Pittsburg/Bay Point': 'pitt', 'Union City': 'ucty', 'Glen Park (SF)': 'glen', "San Francisco Int'l Airport": 'sfia', 'Orinda': 'orin', 'West Dublin': 'wdub', 'Montgomery St. (SF)': 'mont', 'South Hayward': 'shay', 'South San Francisco': 'ssan', 'North Berkeley': 'nbrk'}

def gets_lat_lon_for_stop(stop):

    bart_station_abbr_name = {'Ashby (Berkeley)': 'ashb', 'Powell St. (SF)': 'powl', 'Coliseum': 'cols', 'San Leandro': 'sanl', 'North Concord/Martinez': 'ncon', 'Richmond': 'rich', 'Pleasant Hill': 'phil', '19th St. Oakland': '19th', 'Hayward': 'hayw', '12th St. Oakland City Center': '12th', 'BayFair (San Leandro)': 'bayf', 'Civic Center (SF)': 'civc', 'Castro Valley': 'cast', 'Fremont': 'frmt', 'Lake Merritt (Oakland)': 'lake', 'West Oakland': 'woak', '24th St. Mission (SF)': '24th', 'El Cerrito Plaza': 'plza', 'Millbrae': 'mlbr', 'Colma': 'colm', 'Downtown Berkeley': 'dbrk', 'Balboa Park (SF)': 'balb', 'Embarcadero (SF)': 'embr', 'El Cerrito del Norte': 'deln', 'Dublin/Pleasanton': 'dubl', 'Lafayette': 'lafy', "Oakland Int'l Airport": 'oakl', 'Fruitvale (Oakland)': 'ftvl', '16th St. Mission (SF)': '16th', 'Walnut Creek': 'wcrk', 'MacArthur (Oakland)': 'mcar', 'San Bruno': 'sbrn', 'Rockridge (Oakland)': 'rock', 'Daly City': 'daly', 'Concord': 'conc', 'Pittsburg/Bay Point': 'pitt', 'Union City': 'ucty', 'Glen Park (SF)': 'glen', "San Francisco Int'l Airport": 'sfia', 'Orinda': 'orin', 'West Dublin': 'wdub', 'Montgomery St. (SF)': 'mont', 'South Hayward': 'shay', 'South San Francisco': 'ssan', 'North Berkeley': 'nbrk'}

    bart_station = bart_station_abbr_name[stop]

    if bart_station is None:
            split_stop = stop[0].split("/")
            bart_station = bart_station_abbr_name.get(split_stop[0])

    url = 'http://api.bart.gov/api/stn.aspx?cmd=stninfo&orig=' + bart_station + '&key=' + BART_TOKEN

    response_agencies = requests.get(url)

    agencies_tree = ElementTree.fromstring(response_agencies.text)

    for node in agencies_tree.iter('name'):
        name = node.text

    for node in agencies_tree.iter('gtfs_latitude'):
        lat = node.text

    for node in agencies_tree.iter('gtfs_longitude'):
        lon = node.text

    return (name, lat, lon)


def gets_lat_lon_for_many_stops(stops):

    bart_station_abbr_name ={'downtown berkeley': 'dbrk', 'concord': 'conc', 'pittsburg/bay point': 'pitt', 'san leandro': 'sanl', 'orinda': 'orin', 'dublin/pleasanton': 'dubl', '19th st. oakland': '19th', 'macarthur (oakland)': 'mcar', 'south hayward': 'shay', '12th st. oakland city center': '12th', 'bayfair (san leandro)': 'bayf', 'rockridge (oakland)': 'rock', 'daly city': 'daly', 'civic center (sf)': 'civc', 'castro valley': 'cast', 'coliseum': 'cols', 'union city': 'ucty', 'el cerrito del norte': 'deln', 'north concord/martinez': 'ncon', 'embarcadero (sf)': 'embr', 'richmond': 'rich', 'west dublin': 'wdub', 'north berkeley': 'nbrk', 'el cerrito plaza': 'plza', 'ashby (berkeley)': 'ashb', 'powell st. (sf)': 'powl', 'colma': 'colm', 'fremont': 'frmt', 'lake merritt (oakland)': 'lake', '16th st. mission (sf)': '16th', 'montgomery st. (sf)': 'mont', 'pleasant hill': 'phil', 'south san francisco': 'ssan', 'fruitvale (oakland)': 'ftvl', 'walnut creek': 'wcrk', 'san bruno': 'sbrn', 'millbrae': 'mlbr', 'balboa park (sf)': 'balb', 'glen park (sf)': 'glen', "san francisco int'l airport": 'sfia', 'lafayette': 'lafy', 'west oakland': 'woak', "oakland int'l airport": 'oakl', '24th st. mission (sf)': '24th', 'hayward': 'hayw'}


    stop_info = {}

    for stop in stops:

        print stop

        bart_station = bart_station_abbr_name.get(stop[0].lower())

        if bart_station is None:
            split_stop = stop[0].split("/")
            bart_station = bart_station_abbr_name.get(split_stop[0].lower())

        print bart_station

        url = 'http://api.bart.gov/api/stn.aspx?cmd=stninfo&orig=' + bart_station + '&key=' + BART_TOKEN

        response_agencies = requests.get(url)

        agencies_tree = ElementTree.fromstring(response_agencies.text)

        for node in agencies_tree.iter('name'):
            name = node.text

        for node in agencies_tree.iter('gtfs_latitude'):
            lat = node.text

        for node in agencies_tree.iter('gtfs_longitude'):
            lon = node.text

        stop_info[stop[0].lower()] = (lat, lon)

    return stop_info


"""Get next waypoint with Maps API nearby location search"""
import googlemaps
import json

from config import working_dir, maps_key_fpath


def get_geocode_vitals(gmaps, address=None, place_id=None):
    """Formatted address, latitude, longitude, place_id, and type"""
    if address:
        data = gmaps.geocode(address=address)
    else:
        data = gmaps.geocode(place_id=place_id)
    if not data:
        print('ERROR getting geocode')
    return {
        'address': data[0]['formatted_address'],
        'lat': data[0]['geometry']['location']['lat'],
        'lng': data[0]['geometry']['location']['lng'],
        'place_id': data[0]['place_id'],
        'type': data[0]['types'][0],
    }


def get_maps_client():
    with open(maps_key_fpath, 'r') as fp:
        api_key = fp.read()
    client = googlemaps.Client(key=api_key)
    return client


def get_nearby_vitals(gmaps, origin, target):
    response = gmaps.places_nearby(
        location=(origin['lat'], origin['lng']),
        keyword=target,
        rank_by='distance',
    )
    nearby_result = response.get('results')
    if not nearby_result:
        print('ERROR getting nearby for:')
        print(f'Origin:\n{origin}')
        print(f'Target:\n{target}')
        print('')
    return nearby_result


def get_point_names():
    trans_fpath = f'{working_dir}/transformed.txt'
    with open(trans_fpath, 'r') as fp:
        legs = json.load(fp)
    # Just first leg for now
    data = legs[0]
    points = [data['origin']]
    for wayp in data['waypoints']:
        points.append(wayp)
    points.append(data['destination'])
    print('Points to analyze:')
    for pt in points:
        print(pt)
    print('')
    return points


if __name__ == '__main__':
    gclient = get_maps_client()
    points = get_point_names()
    geodata = [None for i in range(len(points))]

    for i, destination_by_name in enumerate(points):
        if i == 0:
            continue
        origin_by_name = points[i - 1]

        if geodata[i - 1] is None:
            geodata[i - 1] = get_geocode_vitals(gclient, address=points[i - 1])
        origin_geodata = geodata[i - 1]
        print(f"{i}. From {origin_geodata['address']} to {destination_by_name}...")
        origin_geo_json = json.dumps(origin_geodata, indent=4)
        print(f'Origin geodata:\n{origin_geo_json}')

        nearby_result = get_nearby_vitals(gclient, origin_geodata, destination_by_name)

        # nearby_json = json.dumps(nearby_result, indent=4)
        # print(f'Nearby result:\n{nearby_json}')
        geodata[i] = get_geocode_vitals(gclient, place_id=nearby_result[0]['place_id'])
        destination_geo_json = json.dumps(geodata[i], indent=4)
        print(f'Destination geodata:\n{destination_geo_json}')
        print('')

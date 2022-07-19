"""Get next waypoint with Maps API nearby location search"""
import json

from config import working_dir, gmaps


def get_geocode_vitals(address=None, place_id=None, name=''):
    """Formatted address, latitude, longitude, place_id, and type"""
    if address:
        data = gmaps.geocode(address=address)
    else:
        data = gmaps.geocode(place_id=place_id)
    if not data:
        print('ERROR getting geocode')
    return {
        'label': name,
        'address': data[0]['formatted_address'],
        'lat': data[0]['geometry']['location']['lat'],
        'lng': data[0]['geometry']['location']['lng'],
        'place_id': data[0]['place_id'],
        'type': data[0]['types'][0],
    }


def get_nearby_id(origin, target):
    response = gmaps.places_nearby(
        location=(origin['lat'], origin['lng']),
        keyword=target,
        rank_by='distance',
    )
    result = response.get('results')
    if not result:
        raise ValueError(f'ERROR getting nearby for {origin} to {target}')
    return result[0]['place_id']


def get_point_names():
    trans_fpath = f'{working_dir}/transformed.txt'
    with open(trans_fpath, 'r') as fp:
        legs = json.load(fp)
    # TODO: Just first leg for now; when we do all legs, save destination info from one leg as origin for next
    data = legs[0]
    result = [data['origin']]
    for wayp in data['waypoints']:
        result.append(wayp)
    result.append(data['destination'])
    return result


if __name__ == '__main__':
    points = get_point_names()
    geodata = [{} for i in range(len(points))]
    for i, destination_name in enumerate(points):
        if i == 0:      # 1st pass, just get geocode of origin
            geodata[i] = get_geocode_vitals(address=points[i], name=destination_name)
            continue
        print(f"{i}. From {geodata[i - 1]['address']} to {destination_name}...")
        print(f'Origin geodata:\n{json.dumps(geodata[i - 1], indent=4)}')
        nearby_place_id = get_nearby_id(geodata[i - 1], destination_name)
        geodata[i] = get_geocode_vitals(place_id=nearby_place_id, name=destination_name)
        print(f'Destination geodata:\n{json.dumps(geodata[i], indent=4)}')
        print('')
    print(f'Final results:\n{json.dumps(geodata, indent=4)}')
    nearby_fpath = f'{working_dir}/nearby.json'
    with open(nearby_fpath, 'w') as fp:
        json.dump(geodata, fp, indent=4)
    print(f'Wrote {nearby_fpath}.')


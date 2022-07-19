"""Get next waypoint with Maps API nearby location search"""
import json
import os
from time import sleep

from config import working_dir, gmaps


def get_distance(origin_geodata, destination_geodata):
    orig = (origin_geodata['lat'], origin_geodata['lng'])
    dest = (destination_geodata['lat'], destination_geodata['lng'])
    data = gmaps.distance_matrix(
        origins=orig,
        destinations=dest,
        mode='driving',
        units='imperial',
    )
    # print(json.dumps(data, indent=4))
    elem = data["rows"][0]["elements"][0]
    result = f'{elem["distance"]["text"]} ({elem["duration"]["text"]})'
    return result


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


def get_legs():
    trans_fpath = f'{working_dir}/transformed.txt'
    with open(trans_fpath, 'r') as fp:
        legs = json.load(fp)
    results = []
    for leg in legs:
        result = [leg['origin']]
        for wayp in leg['waypoints']:
            result.append(wayp)
        result.append(leg['destination'])
        results.append(result)
    return results


def get_nearby_id(origin, target):
    """Call API to find nearby location we want, then extract place_id Maps's unique place identifier."""
    result = None
    count = 0
    while not result and count < 5:
        if count:
            print('Get nearby failed; sleep...')
            sleep(5)
        count += 1
        response = gmaps.places_nearby(location=(origin['lat'], origin['lng']), keyword=target, rank_by='distance')
        result = response.get('results')
    if not result:
        raise ValueError(f'Failed to get nearby for {origin["address"]} to {target}')
    return result[0]['place_id']


if __name__ == '__main__':
    legs = get_legs()
    alldata = []
    last_dest_geo = None
    for leg_i, points in enumerate(legs):
        leg_no = leg_i + 1
        leg_nearby_fpath = f'{working_dir}/nearby-{leg_no}.json'
        if os.path.exists(leg_nearby_fpath):
            with open(leg_nearby_fpath, 'r') as fp:
                leg_data = json.load(fp)
            last_dest_geo = leg_data[-1]
            print(f'Leg {leg_no} already written ({leg_nearby_fpath}); skipping...')
            continue
        geodata = [{} for x in range(len(points))]
        for dest_no, destination_name in enumerate(points):
            if dest_no == 0:      # Origin; just get geocode and store
                if last_dest_geo is None:
                    geodata[dest_no] = get_geocode_vitals(address=points[dest_no], name=destination_name)
                else:
                    # For origin for this leg, use final destination from last leg
                    geodata[dest_no] = last_dest_geo
                continue
            print(f"Leg {leg_no}, segment {dest_no}. From {geodata[dest_no - 1]['address']} to {destination_name}...")
            # print(f'Origin geodata:\n{json.dumps(geodata[dest_no - 1], indent=4)}')
            # print(f'Origin: {geodata[dest_no - 1]["address"]}')
            nearby_place_id = get_nearby_id(geodata[dest_no - 1], destination_name)
            # Is Google throttling when we make lots of calls quickly? Not sure.
            geodata[dest_no] = get_geocode_vitals(place_id=nearby_place_id, name=destination_name)
            print(f'Destination: {geodata[dest_no]["address"]}')
            distance = get_distance(geodata[dest_no], geodata[dest_no - 1])
            print(f'Distance: {distance}')
            print('')
            sleep(2)
        with open(leg_nearby_fpath, 'w') as fp:
            json.dump(geodata, fp, indent=4)
        print(f'Wrote {leg_nearby_fpath}.')
        last_dest_geo = geodata[-1].copy()
        alldata.append(geodata)
    print(f'Final results:\n{json.dumps(alldata, indent=4)}')
    nearby_fpath = f'{working_dir}/nearby.json'
    with open(nearby_fpath, 'w') as fp:
        json.dump(alldata, fp, indent=4)
    print(f'Wrote {nearby_fpath}.')


# Test getting next waypoint with Maps API nearby location search
import googlemaps
import json


from config import working_dir, maps_key_fpath


with open(maps_key_fpath, 'r') as fp:
    api_key = fp.read()
gmaps = googlemaps.Client(key=api_key)

origin_address = 'Residence Inn by Marriott, 40 Lake Ave., Manchester, NH 03101'
destination_by_name = 'Lake Ave & Granite St'

origin_geocode = gmaps.geocode(address=origin_address)
origin_geo_json = json.dumps(origin_geocode, indent=4)
print(f'Origin geocode:\n{origin_geo_json}')

(origin_lat, origin_lng) = map(origin_geocode[0]['geometry']['location'].get, ('lat', 'lng'))

response = gmaps.places_nearby(
    location=(origin_lat, origin_lng),
    keyword=destination_by_name,
    rank_by='distance',
)
nearby_result = response.get('results')
print(f'Nearby result:\n{nearby_result}')

nearby_fpath = f'{working_dir}/nearby.json'
with open(nearby_fpath, 'w') as fp:
    json.dump(nearby_result, fp, indent=4)
print(f'Wrote {nearby_fpath}.')

destination_geocode = gmaps.geocode(place_id=nearby_result[0]['place_id'])
destination_geo_json = json.dumps(destination_geocode, indent=4)
print(f'Destination geocode:\n{destination_geo_json}')

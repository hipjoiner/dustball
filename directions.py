import googlemaps
import json

from config import working_dir, maps_key_fpath


with open(maps_key_fpath, 'r') as fp:
    api_key = fp.read()
gmaps = googlemaps.Client(key=api_key)
directions_result = gmaps.directions(
    origin='3167 The Oaks Road, Ellicott City, MD',
    destination='950 Cannon Circle, Webster, NY',
    mode='driving',
    waypoints=[
        'Newark International Airport',
    ],
)

directions_fpath = f'{working_dir}/directions.json'
with open(directions_fpath, 'w') as fp:
    json.dump(directions_result, fp=fp, indent=4)
# print(directions_result)
print(f'Wrote {directions_fpath}.')

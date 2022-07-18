"""
Current code below is but a tinker toy.

Process:
Read in transformed.txt
For each mapping set:
    For each origin/waypoint/destination pair:
        Refer to nearby.py for grabbing geocode info and particularly place_id, the unique identifier we want.
        Call geocode on origin for origin geocode data (lat/lng right now)
        Call nearby with origin & next waypt/destination to get known location result
        Call geocode on destination for destination geocode data
        Print out each value as discovered so we can see if/when directions go bad and have to be edited
    Construct waypoints based on geocode place_id values
    Use test.html as a template for a renderable browser page.
    Insert into test.html the route, using place_id values to ensure all valid, resolved map points
"""

import googlemaps
import json

from config import working_dir, maps_key_fpath


origin = 'Residence Inn by Marriott, 40 Lake Ave., Manchester, NH 03101'
destination = 'Main St'


with open(maps_key_fpath, 'r') as fp:
    api_key = fp.read()
gmaps = googlemaps.Client(key=api_key)
directions_result = gmaps.directions(
    origin=origin,
    destination=destination,
    mode='driving',
    waypoints=[
    ],
)

directions_fpath = f'{working_dir}/directions.json'
with open(directions_fpath, 'w') as fp:
    json.dump(directions_result, fp=fp, indent=4)
# print(directions_result)
print(f'Wrote {directions_fpath}.')

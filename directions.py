"""
Complete geocode data for origin/waypoints/destination computed in nearby.py, written to nearby.json
Now, use an html template to produce a renderable browser page.
Into the template html, insert:
    gmaps API key
    origin
    destination
    waypoints
Save as separate html file for loading into browser
"""
import json

from config import working_dir, gmaps_key
from template import html_template

nearby_fpath = f'{working_dir}/nearby.json'
with open(nearby_fpath, 'r') as fp:
    points = json.load(fp)

html = html_template.replace('{API_KEY}', gmaps_key)
html = html.replace('{ORIGIN}', points[0]['place_id'])
html = html.replace('{DESTINATION}', points[-1]['place_id'])
waypoints = []
for wp in points[1:-1]:
    waypoints.append(wp['place_id'])
html = html.replace('{WAYPOINTS}', json.dumps(waypoints, indent=4))

result_fpath = f'{working_dir}/result.html'
with open(result_fpath, 'w') as fp:
    fp.write(html)
print(f'Wrote {result_fpath}.')

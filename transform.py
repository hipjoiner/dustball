"""
From image-scanned raw text, massage text into something clean and formatted
that can be transformed into json
"""
import json
import re

from config import working_dir


do_not_divert = re.compile(re.escape('do not divert'), re.IGNORECASE)


def new_leg():
    return {
        'origin':      None,
        'waypoints':   [],
        'destination': None,
    }


def parse_road(line):
    toks = line.split('.')
    tail = ''.join(toks[1:])
    loc = tail.find(' onto ')
    if loc != -1:
        tail = tail[loc + 5:]
    else:
        loc = tail.find(' on ')
        if loc != -1:
            tail = tail[loc + 3:]
    tail = do_not_divert.sub('', tail)
    road = tail.strip(' ')
    return road


def parse_legs():
    interpreted_fpath = f'{working_dir}/interpreted.txt'
    with open(interpreted_fpath, 'r') as fp:
        lines = fp.read().split('\n')
    legs = []
    leg = new_leg()
    prev_road = None
    for line in lines:
        if line.startswith('S'):
            place = ''.join(line.split('.')[1:]).strip(' ')
            if leg['origin']:
                leg['destination'] = place
                legs.append(leg)
                leg = new_leg()
            if line != lines[-1]:
                leg['origin'] = place
            else:
                legs.append(leg)
        else:
            road = parse_road(line)
            if prev_road:
                intersection = f'{prev_road} & {road}'
                leg['waypoints'].append(intersection)
            prev_road = road
    return legs


def transform_text():
    legs = parse_legs()
    trans_fpath = f'{working_dir}/transformed.txt'
    with open(trans_fpath, 'w') as fp:
        json.dump(legs, fp, indent=4)
    print(f'Wrote {trans_fpath}.')


if __name__ == '__main__':
    transform_text()

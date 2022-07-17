"""
From image-scanned raw text, massage text into something clean and formatted
that can be transformed into json
"""
import json

from config import working_dir


def new_leg():
    return {
        'origin':      None,
        'destination': None,
        'waypoints':   [],
    }


def parse_legs():
    interpreted_fpath = f'{working_dir}/interpreted.txt'
    with open(interpreted_fpath, 'r') as fp:
        lines = fp.read().split('\n')
    legs = []
    leg = new_leg()
    for line in lines:
        if line.startswith('S'):
            stop = ''.join(line.split('.')[1:]).lstrip(' ')
            if leg['origin']:
                leg['destination'] = stop
                legs.append(leg)
                leg = new_leg()
            if line != lines[-1]:
                leg['origin'] = stop
            else:
                legs.append(leg)
        else:
            toks = line.split('.')
            tail = ''.join(toks[1:])
            loc = tail.find(' onto ')
            if loc != -1:
                tail = tail[loc + 5:]
            else:
                loc = tail.find(' on ')
                if loc != -1:
                    tail = tail[loc + 3:]
            wayp = tail
            leg['waypoints'].append(wayp.lstrip(' '))
    return legs


def transform_text():
    legs = parse_legs()
    trans_fpath = f'{working_dir}/transformed.txt'
    with open(trans_fpath, 'w') as fp:
        json.dump(legs, fp, indent=4)
    print(f'Wrote {trans_fpath}.')


if __name__ == '__main__':
    transform_text()

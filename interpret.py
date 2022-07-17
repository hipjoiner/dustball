"""
From image-scanned raw text, massage text into something clean and formatted
that can be transformed into json
"""
import re

from config import working_dir


line_contains_filters = [
    'NAVIGATION',
]

line_starts_filters = [
    'Welcome',
    'Group meeting',
    'Driving etiquette',
    'D:',
    'S:',
    'Lunch: Lunch',
    'Fuel:',
    '•',
    'Please ',
    'Pictures ',
]

line_starts_exprs = [
    re.compile('^S\d+\.'),
    re.compile('^D\d+\.')
]


def interpret_text():
    scan_fpath = f'{working_dir}/scanned.txt'
    with open(scan_fpath, 'r') as fp:
        raw_lines = fp.read().split('\n')
    body = ['S0.']
    for line in raw_lines:
        omit = False
        for tok in line_contains_filters:
            if tok in line:
                omit = True
                break
        for tok in line_starts_filters:
            if line.startswith(tok):
                omit = True
                break
        if omit:
            continue
        match = False
        for expr in line_starts_exprs:
            if expr.match(line):
                match = True
        if match:
            body.append(line)
        else:
            body[-1] = f'{body[-1]} {line}'
    text_fpath = f'{working_dir}/interpreted.txt'
    with open(text_fpath, 'w') as fp:
        fp.write('\n'.join(body))
    print(f'Wrote {text_fpath}.')


if __name__ == '__main__':
    interpret_text()

"""
From image-scanned raw text, massage text into something clean and formatted
that can be transformed into json
"""

from config import working_dir


directions_fpath = f'{working_dir}/directions-edited.txt'
with open(directions_fpath, 'r') as fp:
    lines = fp.read().split('\n')

for line in lines:
    print(line)

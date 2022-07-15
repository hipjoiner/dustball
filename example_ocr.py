import io
import os
from google.cloud import vision


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.y},{self.x})'


class Symbol:
    def __init__(self, gsymbol):
        self.gsymbol = gsymbol
        self.tl = None
        self.lr = None
        self.text = gsymbol.text


def parse_symbol(symbol):
    poly = symbol.bounding_box
    minx = 1e6
    miny = 1e6
    maxx = 0
    maxy = 0
    for v in poly.vertices:
        # print(v)
        if v.x < minx:
            minx = v.x
        elif v.x > maxx:
            maxx = v.x
        if v.y < miny:
            miny = v.y
        elif v.y > maxy:
            maxy = v.y
    line = f'({minx},{miny}) ({maxx},{maxy}) {symbol.text}'
    return line


def detect_text(fpath):
    """Detects text in the file."""
    with io.open(fpath, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    client = vision.ImageAnnotatorClient()
    response = client.document_text_detection(image=image)
    # response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(response.error.message)
    document = response.full_text_annotation
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        data = parse_symbol(symbol)
                        print(data)
    return document
    # print(texts)
    # text = texts[0]             # First one appears to be all text; others look like sub-groups?
    # return text.description


def main():
    test_dir = 'C:/Users/John/Documents/src/dustball/local'
    cred_fpath = f'{test_dir}/valiant-broker-355912-67d74ed7957a.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_fpath

    images = sorted([entry.path.replace('\\', '/') for entry in os.scandir(test_dir) if entry.name.endswith('.jpg')])
    for jpg_path in images:
        print(f'{jpg_path}:')
        result = detect_text(jpg_path)
        # out_path = jpg_path.replace('.jpg', '.txt')
        # with open(out_path, 'w') as fp:
        #     fp.write(str(result))
        # print(result)
        print('')


if __name__ == '__main__':
    main()

import io
import os
from google.cloud import vision


x_increases_l_to_r = True
y_increases_t_to_b = True


class Line:
    def __init__(self, word=None):
        self.words = []
        self.y_min = 1e6
        self.y_max = 0
        self.x_min = 1e6
        self.x_max = 0
        if word:
            self.append(word)

    def __str__(self):
        return self.text

    def append(self, word):
        self.words.append(word)
        self.x_min = min(self.x_min, word.x_min)
        self.x_max = max(self.x_max, word.x_max)
        self.y_min = min(self.y_min, word.y_min)
        self.y_max = max(self.y_max, word.y_max)

    def takes(self, word):
        """Is this word on this line?"""
        if not self.words:
            return True
        # if y_increases_t_to_b:
        #     return self.y_max < word.y_min and word.y_max < self.y_min
        # else:
        return self.y_min < word.y_max and word.y_min < self.y_max

    @property
    def text(self):
        return ' '.join([word.text for word in self.words])


class Word:
    def __init__(self, gword):
        self.text = ''
        self.y_min = 1e6
        self.y_max = 0
        self.x_min = 1e6
        self.x_max = 0
        for symbol in gword.symbols:
            self.text = f'{self.text}{symbol.text}'
            poly = symbol.bounding_box
            for v in poly.vertices:
                self.x_min = min(self.x_min, v.x)
                self.x_max = max(self.x_max, v.x)
                self.y_min = min(self.y_min, v.y)
                self.y_max = max(self.y_max, v.y)

    def __lt__(self, other):
        """Logic depends on whether coordinates are increasing or decreasing from top to bottom
        I don't yet know why they vary from one image to the next.  Rotation?
        """
        if self.y_max < other.y_min:
            return y_increases_t_to_b
        elif other.y_max < self.y_min:
            return not y_increases_t_to_b
        if self.x_min < other.x_min:
            return x_increases_l_to_r
        return not x_increases_l_to_r

    def __repr__(self):
        return f'{self.text} {self.y_min}-{self.y_max} {self.x_min}-{self.x_max}'

    def __str__(self):
        return self.text

    def append(self, append_word):
        self.text = f'{self.text}{append_word.text}'
        self.x_min = min(self.x_min, append_word.x_min)
        self.x_max = max(self.x_max, append_word.x_max)
        self.y_min = min(self.y_min, append_word.y_min)
        self.y_max = max(self.y_max, append_word.y_max)


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
    return document


def form_words(document):
    raw = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                # print(paragraph)
                for word in paragraph.words:
                    w = Word(word)
                    raw.append(w)
                # print('')
    words = []
    for w in raw:
        if w.text in ['.', ',', ':', '-', ')']:
            words[-1].append(w)
        elif words and words[-1].text.endswith(('(', '-', '~', '•')):
            words[-1].append(w)
        else:
            words.append(w)
    words = sorted(words)
    return words


def form_lines(words):
    lines = []
    line = Line()
    for word in words:
        if line.takes(word):
            line.append(word)
        else:
            lines.append(line)
            line = Line(word)
    if line.words:
        lines.append(line)
    return lines


def show_words(words):
    print(f' Ymin  Ymax  Xmin  Xmax Word        ')
    print(f'----------- ----------- ------------')
    for word in words:
        print(f'{word.y_min:5}-{word.y_max:5} {word.x_min:5}-{word.x_max:5} {word.text:12}')
    print('')


def show_lines(lines):
    print(f' Ymin  Ymax  Xmin  Xmax Line        ')
    print(f'----------- ----------- ------------')
    for line in lines:
        print(f'{line.y_min:5}-{line.y_max:5} {line.x_min:5}-{line.x_max:5} {line.text:12}')
    print('')


def main():
    test_dir = 'C:/Users/John/OneDrive/src/dustball/local'
    cred_fpath = f'{test_dir}/valiant-broker-355912-67d74ed7957a.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_fpath

    images = sorted([entry.path.replace('\\', '/') for entry in os.scandir(test_dir) if entry.name.endswith('.jpg')])
    body = []
    for jpg_path in images:
        print(f'Loading {jpg_path}...')
        document = detect_text(jpg_path)
        words = form_words(document)
        lines = form_lines(words)
        for line in lines:
            body.append(line.text)
        # print('')
        # body.extend(lines)
    for line in body:
        print(line)
    text_fpath = f'{test_dir}/directions.txt'
    with open(text_fpath, 'w') as fp:
        fp.write('\n'.join(body))


if __name__ == '__main__':
    main()

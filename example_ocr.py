import io
import os
from google.cloud import vision


def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    for text in texts:
        print('\n"{}"'.format(text.description))
        vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


if __name__ == '__main__':
    path = 'C:/Users/John/Documents/src/dustball/local'
    cred_fpath = f'{path}/valiant-broker-355912-67d74ed7957a.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_fpath

    f = 'PXL_20220714_141727282.jpg'
    detect_text(f'{path}/{f}')

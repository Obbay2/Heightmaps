from PIL import Image
import json
from enum import Enum


class TYPE(Enum):
    JSON = 1
    PYTHON = 2


# end is not inclusive
def get_variable_heightmap_data(heightmap_filename: str, start: int, end: int,  type: TYPE):
    metadata = get_heightmap_metadata(heightmap_filename, TYPE.PYTHON)
    metadata['height'] = end - start
    metadata['data'] = []

    for i in range(start, end):
        row_data = get_heightmap_row_data(heightmap_filename, i, TYPE.PYTHON)
        metadata['data'].append(row_data['data'])

    return handle_type_return(metadata, type)


def get_heightmap_row_data(heightmap_filename: str, row_number: int, type: TYPE):
    f = Image.open(heightmap_filename)
    rgb_f = f.convert('L')

    output = dict()
    output['length'] = rgb_f.width
    output['data'] = []

    for x in range(rgb_f.width):
        value = rgb_f.getpixel((x, row_number))
        output['data'].append(value)

    return handle_type_return(output, type)


def get_heightmap_metadata(heightmap_filename: str, type: TYPE):
    image = Image.open(heightmap_filename)

    output = dict()
    output['height'] = image.height
    output['width'] = image.width

    return handle_type_return(output, type)


def handle_type_return(python_obj: dict, type: TYPE):
    if type == TYPE.JSON:
        return json.dumps(python_obj)
    elif type == TYPE.PYTHON:
        return python_obj

from PIL import Image
import json
from enum import Enum
import numpy as np


class TYPE(Enum):
    JSON = 1
    PYTHON = 2


def get_voxel_data(heightmap_filename: str, start: int, end: int,  resolution: float, waterLevel: int, type: TYPE):
    flat_data = get_variable_heightmap_data(heightmap_filename, start, end, resolution, TYPE.PYTHON)

    flat_data['data'] = np.array(flat_data['data'])
    max_data_height = int(np.amax(flat_data['data']))

    flat_data['height'] = max_data_height
    flat_data['length'] = end - start

    if max_data_height == 0:
        flat_data['height'] = waterLevel
        flat_data['data'] = np.ones((flat_data['data'].shape[0], waterLevel, flat_data['data'].shape[1])).tolist()
        return handle_type_return(flat_data, type)
    else:
        water_data = np.ones((flat_data['data'].shape[0], waterLevel, flat_data['data'].shape[1]))

        for h in range(waterLevel, max_data_height):
            new_plane = np.zeros((flat_data['data'].shape[0], flat_data['data'].shape[1]))

            for i in range(new_plane.shape[0]):
                for j in range(new_plane.shape[1]):
                    if flat_data['data'][i][j] >= h:
                        new_plane[i][j] = 1

            reshape = np.reshape(new_plane, (new_plane.shape[0], 1, new_plane.shape[1]))
            water_data = np.append(water_data, reshape, axis=1)

        flat_data['data'] = water_data.tolist()
        return handle_type_return(flat_data, type)


# end is not inclusive
def get_variable_heightmap_data(heightmap_filename: str, start: int, end: int, resolution: float, type: TYPE):
    f = Image.open(heightmap_filename)
    f = f.resize((int(f.width * resolution), int(f.height * resolution)))
    grayscale_image = f.convert('L')

    metadata = get_heightmap_metadata(heightmap_filename, resolution, TYPE.PYTHON)
    metadata['height'] = end - start
    vertically_scaled_image = np.array(grayscale_image) * resolution
    metadata['data'] = vertically_scaled_image[start:end].tolist()

    f.close()
    grayscale_image.close()
    return handle_type_return(metadata, type)


# Get the number of bytes required to transmit voxel data
def get_voxel_metadata(heightmap_filename: str, resolution: float, type: TYPE):
    data = get_variable_heightmap_data(heightmap_filename, 0,
                                       get_heightmap_metadata(heightmap_filename, 1, TYPE.PYTHON)["height"],
                                       resolution, TYPE.PYTHON)

    npdata = np.array(data['data'])
    max_height = np.amax(npdata)

    output = dict()
    output["B"] = float(max_height * float(npdata.shape[0] * npdata.shape[1]))
    output["MB"] = output["B"] * 0.000001

    return handle_type_return(output, type)


def get_heightmap_metadata(heightmap_filename: str, resolution: float, type: TYPE):
    image = Image.open(heightmap_filename)
    image = image.resize((int(image.width * resolution), int(image.height * resolution)))

    output = dict()
    output['height'] = image.height
    output['width'] = image.width

    image.close()
    return handle_type_return(output, type)


def handle_type_return(python_obj: dict, type: TYPE):
    if type == TYPE.JSON:
        return json.dumps(python_obj)
    elif type == TYPE.PYTHON:
        return python_obj

import re
import numpy as np
from PIL import Image
import base64
from io import BytesIO


def string_to_list(string_of_int):
    """
    Takes a string of integers, divided by coma and
    returns a list of integers.
    """
    list_str = re.sub("[^0-9]", " ", string_of_int).split()
    return list(map(int, list_str))


def image_to_str(np_3d_array):
    """
    Takes a 3 dimensional numpy array and
    returns a string for picture for inserting in HTML file.
    """
    pil_image = Image.fromarray(np_3d_array.astype(np.uint8))
    buff = BytesIO()
    pil_image.save(buff, format="PNG")
    return base64.b64encode(buff.getvalue()).decode("ascii")


def best_worse_predictions(np_array, n):
    """
    Takes a numpy 2d array and
    returns a tuple of n most preferable and not preferable indexes.
    """
    ind_sort = np_array.argsort(axis=0)
    best = ind_sort[:, 0][::-1]
    worse = ind_sort[:, 1]
    return best[:n], worse[:n]

import pytest
import numpy as np
from service.image_actions import string_to_list, best_worse_predictions


@pytest.fixture
def example_array_image():
    """
    Example values of string of numpy array and
    a list of integers.
    """
    return '[234, 2, 50, 140, 230]', [234, 2, 50, 140, 230]


@pytest.fixture
def example_np_predictions():
    """
    Returns a 2d numpy array with example of predictions.
    """
    return np.array([[0.7, 0.3], [1.0, 0], [0.5, 0.5], [0.75, 0.25],
                     [0.33, 0.66], [0.8, 0.2], [0.6, 0.4]])


def test_string_to_list(example_array_image):
    assert string_to_list(example_array_image[0]) == example_array_image[1]


def test_predictions(example_np_predictions):
    best, worse = best_worse_predictions(example_np_predictions, 3)
    assert np.array_equal(best, [1, 5, 3])
    assert np.array_equal(worse, [4, 2, 6])

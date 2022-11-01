from random import sample
from database.get_mongodb import get_mongodb
from collections import OrderedDict
import numpy as np
from service.train import train_and_predict
import re
from service.image_actions import string_to_list


class UserChoice:
    def __init__(self):
        self.db = get_mongodb()
        total_dresses = self.db.dresses.objects.count_documents({})
        self.id_images = sample(range(0, total_dresses), 10)
        self.cursor = self.db.dresses.objects.find(
            {'id_image': {'$in': self.id_images}},
            {'values': 1, '_id': 0, 'id_image': 1}
        )
        self.np_colors = OrderedDict()
        self.result = OrderedDict()

    async def result_calc(self):
        if len(self.np_colors) != len(self.result):
            raise ValueError("Length of results should be equal!")

        im_array = np.array([np.asarray(img).flatten() for id, img in self.np_colors.items()], dtype=int)
        result_array = np.array([res for id, res in self.result.items()], dtype=int)

        rest_images = list(self.db.dresses.objects.find(
            {'id_image': {'$nin': self.id_images}},
            {'values': 1, '_id': 0}
        ))

        np_others = np.empty((0, 339360), int)
        for im in rest_images:
            temp_arr = [string_to_list(im['values'])]
            np_others = np.append(np_others, temp_arr, axis=0)

        self.prediction = train_and_predict(im_array, result_array, np_others)

        print(self.prediction)


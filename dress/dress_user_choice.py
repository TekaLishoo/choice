from random import sample
from database.get_mongodb import get_mongodb
from collections import OrderedDict
import numpy as np
from service.train import train_and_predict
from service.image_actions import string_to_list, best_worse_predictions, image_to_str


class UserChoice:
    def __init__(self):
        self.db = get_mongodb()
        total_dresses = self.db.dresses.objects.count_documents({})
        self.id_images = sample(range(0, total_dresses), 10)
        self.cursor = self.db.dresses.objects.find(
            {"id_image": {"$in": self.id_images}},
            {"values": 1, "_id": 0, "id_image": 1},
        )
        self.np_colors = OrderedDict()
        self.result = OrderedDict()

    async def result_calc(self):
        if len(self.np_colors) != len(self.result):
            raise ValueError("Length of results should be equal!")

        im_array = np.array(
            [np.asarray(img).flatten() for id, img in self.np_colors.items()], dtype=int
        )
        result_array = np.array([res for id, res in self.result.items()], dtype=int)

        self.rest_images = list(
            self.db.dresses.objects.find(
                {"id_image": {"$nin": self.id_images}},
                {"values": 1, "_id": 0, "id_image": 1},
            )
        )

        np_others = np.empty((0, 339360), int)
        for im in self.rest_images:
            temp_arr = [string_to_list(im["values"])]
            np_others = np.append(np_others, temp_arr, axis=0)

        prediction = train_and_predict(im_array, result_array, np_others)

        best, worse = best_worse_predictions(prediction, 6)
        print(best, worse)

        best_list = []
        worse_list = []
        for id in best:
            np_array_reshaped = np_others[id].reshape(404, 280, 3)
            best_list.append(image_to_str(np_array_reshaped))

        for id in worse:
            np_array_reshaped = np_others[id].reshape(404, 280, 3)
            worse_list.append(image_to_str(np_array_reshaped))

        return best_list, worse_list

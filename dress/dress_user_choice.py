from random import sample
from database.get_mongodb import get_mongodb


class UserChoice:
    def __init__(self):
        db = get_mongodb()
        total_dresses = db.dresses.objects.count_documents({})
        self.id_images = sample(range(0, total_dresses), 10)
        self.cursor = db.dresses.objects.find(
            {'id_image': {'$in': self.id_images}},
            {'values': 1, '_id': 0, 'id_image': 1}
        )
        self.result = dict()



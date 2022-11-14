from pymongo import MongoClient
from config.config import Settings


settings = Settings()


def get_mongodb():
    return MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

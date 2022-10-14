from pymongo import MongoClient
from config.config import Settings
from fastapi import Depends


def get_mongodb(settings=Depends(Settings)):
    return MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)


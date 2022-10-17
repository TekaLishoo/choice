from fastapi import APIRouter, Depends
from pydantic.validators import List
from dress.routers_dresses.schemas_dresses import DressDisplay
from database.get_mongodb import get_mongodb
from pymongo import MongoClient
from logging_conf import setup_logger


router = APIRouter(prefix='/dresses', tags=['dresses', ])


@router.get('', response_model=List[DressDisplay])
def rout_list_dresses(db: MongoClient = Depends(get_mongodb)):
    dresses = db.dresses.objects.find()
    return list(dresses)

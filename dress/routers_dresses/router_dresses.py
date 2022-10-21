from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pydantic.validators import List
from dress.routers_dresses.schemas_dresses import DressDisplay
from database.get_mongodb import get_mongodb
from pymongo import MongoClient


router = APIRouter(prefix='/dresses', tags=['dresses', ])
templates = Jinja2Templates(directory='dress/templates')


@router.get('', response_model=List[DressDisplay])
def rout_list_dresses(db: MongoClient = Depends(get_mongodb)):
    dresses = db.dresses.objects.find()
    return list(dresses)


@router.get('/choice', response_class=HTMLResponse)
def choice_dress_front(request: Request):
    return templates.TemplateResponse("dresschoicechoice.html", {'request': request})


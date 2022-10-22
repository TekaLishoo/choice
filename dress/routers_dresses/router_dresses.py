from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pydantic.validators import List
import re
import numpy as np
from PIL import Image
import base64
from io import BytesIO
from dress.routers_dresses.schemas_dresses import DressDisplay
from database.get_mongodb import get_mongodb
from pymongo import MongoClient
from dress.dress_user_choice import UserChoice


router = APIRouter(prefix='/dresses', tags=['dresses', ])
templates = Jinja2Templates(directory='dress/templates')
user_choice = UserChoice()


@router.get('', response_model=List[DressDisplay])
def rout_list_dresses(db: MongoClient = Depends(get_mongodb)):
    dresses = db.dresses.objects.find()
    return list(dresses)


@router.get('/choice', response_class=HTMLResponse)
def choice_dress_front(request: Request):
    print(user_choice.id_images)
    image_info = next(user_choice.cursor)
    print(image_info['id_image'])
    list_str = re.sub("[^0-9]", " ",  image_info['values']).split()
    array_colors = list(map(int, list_str))
    np_array_colors = np.array(array_colors).reshape(404, 280, 3)
    pil_image = Image.fromarray(np_array_colors.astype(np.uint8))

    buff = BytesIO()
    pil_image.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue()).decode('ascii')
    return templates.TemplateResponse("dresschoicechoice.html", {'request': request, 'images': img_str})


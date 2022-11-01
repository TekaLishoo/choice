from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pydantic.validators import List
import numpy as np
from PIL import Image
import base64
from io import BytesIO
from dress.routers_dresses.schemas_dresses import DressDisplay
from database.get_mongodb import get_mongodb
from pymongo import MongoClient
from dress.dress_user_choice import UserChoice
from service.image_actions import string_to_list, image_to_str

router = APIRouter(prefix='/dresses', tags=['dresses', ])
templates = Jinja2Templates(directory='dress/templates')
user_choice = UserChoice()


@router.get('', response_model=List[DressDisplay])
def rout_list_dresses(db: MongoClient = Depends(get_mongodb)):
    dresses = db.dresses.objects.find()
    return list(dresses)


@router.get('/choice', response_class=HTMLResponse)
async def choice_dress_front(request: Request):
    if user_choice.cursor.alive:
        image_info = next(user_choice.cursor)
        user_choice.np_colors[image_info['id_image']] = string_to_list(image_info['values'])
        np_array_reshaped = np.array(user_choice.np_colors[image_info['id_image']]).reshape(404, 280, 3)
        img_str = image_to_str(np_array_reshaped)

        return templates.TemplateResponse("dresschoicechoice.html", {
            'request': request,
            'images': img_str,
            'id_image': image_info['id_image'],
        })
    else:
        await user_choice.result_calc()
        return templates.TemplateResponse("dresses_result.html", {
            'request': request,
        })


@router.post('/choice/like/{id_image}')
def add_like(request: Request, id_image: int):
    user_choice.result[id_image] = 1
    return RedirectResponse(url=request.url_for("choice_dress_front"), status_code=302)


@router.post('/choice/dislike/{id_image}')
def add_like(request: Request, id_image: int):
    user_choice.result[id_image] = 0
    return RedirectResponse(url=request.url_for("choice_dress_front"), status_code=302)


@router.get('/result', response_class=HTMLResponse)
def dress_result(request: Request):
    return templates.TemplateResponse("dresses_result.html", {
        'request': request,
    })

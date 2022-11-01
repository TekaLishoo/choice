from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from scheduler import app as app_rocketry
from users.routers_users import router_users
from dress.routers_dresses import router_dresses
from dress.dress_user_choice import UserChoice
from users.db_users import models_users
from database import engine


app = FastAPI()
session = app_rocketry.session

app.include_router(router_users.router)
app.include_router(router_dresses.router)

app.mount(
    "/dress/templates/static",
    StaticFiles(directory="dress/templates/static"),
    name="static",
)

models_users.Base.metadata.create_all(engine)
user_choice = UserChoice()


@app.get(
    "/tasks",
    tags=[
        "periodic tasks",
    ],
)
async def read_tasks():
    return list(session.tasks)

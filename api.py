from fastapi import FastAPI
from scheduler import app as app_rocketry
from users.routers import router_users
from users.db_users import models_users
from database import engine


app = FastAPI()
session = app_rocketry.session

app.include_router(router_users.router)

models_users.Base.metadata.create_all(engine)


@app.get('/')
async def main_menu():
    return {'message': 'Will appear'}


@app.get("/tasks")
async def read_tasks():
    return list(session.tasks)
from fastapi import FastAPI, BackgroundTasks
from users.db_users import models_users
from database import engine
from users.routers import router_users
from dress.load_dresses import LoadDresses


app = FastAPI()

app.include_router(router_users.router)

models_users.Base.metadata.create_all(engine)

dress_handle = LoadDresses()


@app.get("/")
async def startup_load_dresses(background_tasks: BackgroundTasks):
    background_tasks.add_task(dress_handle.load)

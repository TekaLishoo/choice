from fastapi import FastAPI, BackgroundTasks
from fastapi_utils.tasks import repeat_every
from users.db_users import models_users
from database import engine
from users.routers import router_users
from dress.update_dresses import update_dresses

app = FastAPI()

app.include_router(router_users.router)

models_users.Base.metadata.create_all(engine)


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)
async def update_dresses_periodically():
    print('Dresses uploading process has been started')
    update_dresses()



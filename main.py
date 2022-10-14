from fastapi import FastAPI, BackgroundTasks
from users.db_users import models_users
from database import engine
from users.routers import router_users
from dress.update_dresses import update_dresses

app = FastAPI()

app.include_router(router_users.router)

models_users.Base.metadata.create_all(engine)


@app.get("/update_dresses")
async def startup_load_dresses(background_tasks: BackgroundTasks):
    background_tasks.add_task(update_dresses)

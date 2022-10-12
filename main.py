from fastapi import FastAPI
from users.db_users import models_users
from database import engine
from users.routers import router_users


app = FastAPI()

app.include_router(router_users.router)

models_users.Base.metadata.create_all(engine)

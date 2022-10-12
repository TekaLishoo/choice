from fastapi import FastAPI
from users.db_users import models_users
from database import engine


app = FastAPI()

models_users.Base.metadata.create_all(engine)

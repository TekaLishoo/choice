from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_NAME_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str

    MONGO_USER: str
    MONGO_PASS: str
    MONGO_DB: str
    MONGO_HOST: str
    MONGO_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
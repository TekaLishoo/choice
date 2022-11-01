from pydantic import BaseModel


class DressDisplay(BaseModel):
    id_image: int
    values: str

    class Config:
        orm_mode = True

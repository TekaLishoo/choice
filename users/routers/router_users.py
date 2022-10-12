from fastapi import APIRouter, Depends
from users.routers.schemas_users import UserDisplay, UserBase
from sqlalchemy.orm.session import Session
from database import get_db
from users.db_users.db_actions_users import create_user


router = APIRouter(prefix='/users', tags=['users',])


@router.post('/add', response_model=UserDisplay)
def rout_create_user(request: UserBase, db: Session = Depends(get_db)):
    return create_user(db, request)

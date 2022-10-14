from sqlalchemy.orm.session import Session
from users.routers.schemas_users import UserBase
from users.db_users.models_users import ChUser
from users.db_users.hashing import Hash


def create_user(db: Session, request: UserBase):
    new_user = ChUser(
        username=request.username,
        email=request.email,
        password=Hash().bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

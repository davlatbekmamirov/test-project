from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

from database.config import Session, engine
from utils import jwt_required, find_user

user_router = APIRouter(
    prefix="/user",
    tags=['User']
)

session = Session(bind=engine)


@user_router.get('/profile', status_code=status.HTTP_200_OK)
def my_profile(Authorize: AuthJWT = Depends()):
    jwt_required(Authorize)
    username = Authorize.get_jwt_subject()
    db_user = find_user(username, session)
    return jsonable_encoder(db_user)

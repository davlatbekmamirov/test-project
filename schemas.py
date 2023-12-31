from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = '53d47db13355ca13f707ea8dfebee0aec9115c9ecd3f56ad3f905fa23980b090'


class LoginModel(BaseModel):
    username: str
    password: str


class ProfileModel(BaseModel):
    username: str
    email: str


class PostModel(BaseModel):
    id: Optional[int]
    body: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "body": "text ",
            }
        }

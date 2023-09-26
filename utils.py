from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from models.users import User
from models.post import Post


def check_if_email_already_used(user_email: str, session: Session):
    db_email = session.query(User).filter(User.email == user_email).first()

    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    return db_email


def check_if_username_already_used(user_username: str, session: Session):
    db_username = session.query(User).filter(User.username == user_username).first()

    if db_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )
    return db_username


def create_new_user(user_username: str, user_email: str, user_password: str, user_is_staff: bool, user_is_active: bool):
    new_user = User(
        username=user_username,
        email=user_email,
        password=generate_password_hash(user_password),
        is_staff=user_is_staff,
        is_active=user_is_active
    )
    return new_user


def find_user(user_username: str, session: Session):
    db_user = session.query(User).filter(User.username == user_username).first()
    return db_user


def check_if_user_exists_and_check_password(user_username, user_password, db_user: User):
    if not db_user or not check_password_hash(db_user.password, user_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Username or Password"
        )


def response_token(access_token: str, refresh_token: str):
    response = {
        "access": access_token,
        "refresh": refresh_token
    }
    return response


def jwt_required(Authorize: AuthJWT):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )


def find_current_user(Authorize: AuthJWT, session: Session):
    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    return user


def find_user_post_by_id(id: int, session: Session):
    post = session.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post with the given ID doesn't exist"
        )
    return post


def response_post(id: int, body: str, created_at, updated_at=None):
    response = {
        "id": id,
        "body": body,
        "created_at": created_at
    }
    if updated_at is None:
        response["updated_at"] = updated_at
    return response


def check_if_user_is_staff(is_staff: bool):
    if not is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )


def check_post_ownership_or_staff(post_id: int, user_id: int, is_staff: bool):
    if post_id != user_id and not is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This isn't your post!"
        )


def create_post(body: str, user: User):
    new_order = Post(
        body=body
    )
    new_order.user = user
    return new_order

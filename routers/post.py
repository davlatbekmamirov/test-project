import datetime

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

from database.config import Session, engine
from models.post import Post
from schemas import PostModel
from utils import (check_post_ownership_or_staff,
                   create_post, find_current_user, find_user_post_by_id,
                   jwt_required, response_post)

post_router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

session = Session(bind=engine)


@post_router.post('/', status_code=status.HTTP_201_CREATED)
def place_an_order(post: PostModel, Authorize: AuthJWT = Depends()):
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)

    new_order = create_post(post.body, user)

    session.add(new_order)
    session.commit()

    return jsonable_encoder(
        response_post(
            new_order.id, new_order.body, new_order.created_at,
        )
    )


@post_router.get('/')
def list_all_posts():
    posts = session.query(Post).all()
    if not posts:
        return {"message": "No orders were made yet"}

    return jsonable_encoder(posts)


@post_router.get('/{id}')
def get_order_by_id(id: int):
    post = find_user_post_by_id(id, session)

    return jsonable_encoder(post)


@post_router.get('/my_posts/')
def get_user_posts(Authorize: AuthJWT = Depends()):
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)

    if not user.posts:
        return {"message": "You haven't made any posts yet"}

    return jsonable_encoder(user.posts)


@post_router.get('/my_posts/{id}')
def get_user_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)

    return find_user_post_by_id(id, session)


@post_router.put('/{id}')
def update_post_by_id(id: int, post: PostModel, Authorize: AuthJWT = Depends()):
    jwt_required(Authorize)

    post_to_update = find_user_post_by_id(id, session)

    user = find_current_user(Authorize, session)

    check_post_ownership_or_staff(post_to_update.id, user.id, user.is_staff)

    post_to_update.body = post.body
    post_to_update.updated_at = datetime.datetime.now()

    session.commit()

    return jsonable_encoder(
        response_post(
            post_to_update.id, post_to_update.body, post_to_update.created_at, post_to_update.updated_at
        )
    )


@post_router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_an_order(id: int, Authorize: AuthJWT = Depends()):
    jwt_required(Authorize)

    user = find_current_user(Authorize, session)

    order_to_delete = find_user_post_by_id(id, session)

    check_post_ownership_or_staff(order_to_delete.id, user.id, user.is_staff)

    session.delete(order_to_delete)
    session.commit()

    return {"message": "Post successfully deleted"}

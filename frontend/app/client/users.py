from .main import openapi
from app.models import (
    APIError,
    Message,
    UpdatePassword,
    UserCreate,
    UserPublic,
    UserUpdate,
    UserUpdateMe,
    UsersPublic,
)
from . import APIException


def read_users(skip: int = 0, limit: int = 100) -> UsersPublic:
    response = openapi.get(f"/api/v1/users/?skip={skip}&limit={limit}")
    if response.status_code == 200:
        return UsersPublic.model_validate_json(response.content)
    else:
        raise APIException(APIError.model_validate_json(response.content))


def create_user(userdata: UserCreate) -> UserPublic:
    response = openapi.post("/api/v1/users/", data=userdata.model_dump_json())
    if response.status_code == 200:
        user = UserPublic.model_validate_json(response.content)
        return user
    else:
        raise APIException(APIError.model_validate_json(response.content))


def get_user_by_id(user_id: int) -> UserPublic:
    response = openapi.get(f"/api/v1/users/{user_id}")
    if response.status_code == 200:
        user = UserPublic.model_validate_json(response.content)
        return user
    else:
        raise APIException(APIError.model_validate_json(response.content))


def update_user(user_id: int, data: UserUpdate) -> UserPublic:
    response = openapi.patch(
        f"/api/v1/users/{user_id}", data=data.model_dump_json(exclude_none=True)
    )
    if response.status_code == 200:
        user = UserPublic.model_validate_json(response.content)
        return user
    else:
        raise APIException(APIError.model_validate_json(response.content))


def delete_user(user_id: int) -> Message:
    response = openapi.delete(f"/api/v1/users/{user_id}")
    if response.status_code == 200:
        message = Message.model_validate_json(response.content)
        return message
    else:
        raise APIException(APIError.model_validate_json(response.content))


def read_user_me() -> UserPublic:
    response = openapi.get("/api/v1/users/me")
    if response.status_code == 200:
        user = UserPublic.model_validate_json(response.content)
        return user
    else:
        raise APIException(APIError.model_validate_json(response.content))


def update_user_me(user: UserUpdateMe) -> UserPublic:
    response = openapi.patch(
        "/api/v1/users/me", data=user.model_dump_json(exclude_none=True)
    )
    if response.status_code == 200:
        return UserPublic.model_validate_json(response.content)
    else:
        raise APIException(APIError.model_validate_json(response.content))


def delete_user_me() -> Message:
    response = openapi.delete("/api/v1/users/me")
    if response.status_code == 200:
        return Message.model_validate_json(response.content)
    else:
        raise APIException(APIError.model_validate_json(response.content))


def update_password_me(data: UpdatePassword) -> Message:
    response = openapi.patch(
        "/api/v1/users/me/password", data=data.model_dump_json(exclude_none=True)
    )
    if response.status_code == 200:
        return Message.model_validate_json(response.content)
    else:
        raise APIException(APIError.model_validate_json(response.content))

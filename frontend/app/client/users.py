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


def read_users(page: int = 1, limit: int = 100) -> UsersPublic:
    response = openapi.get(f"/users?page={page}&limit={limit}")
    if response.status_code == 200:
        return UsersPublic.model_validate_json(response.content)
    else:
        raise APIException(APIError.model_validate_json(response.content))


def create_user(userdata: UserCreate) -> UserPublic:
    response = openapi.post("/users", data=userdata.model_dump_json())
    if response.status_code == 200:
        user = UserPublic.model_validate_json(response.content)
        return user
    else:
        raise APIException(APIError.model_validate_json(response.content))


def get_user_by_id(user_id: str) -> UserPublic:
    response = openapi.get(f"/users/{user_id}")
    if response.status_code == 200:
        user = UserPublic.model_validate_json(response.content)
        return user
    else:
        raise APIException(APIError.model_validate_json(response.content))


def update_user(user_id: str, data: UserUpdate) -> UserPublic:
    response = openapi.patch(
        f"/users/{user_id}", data=data.model_dump_json(exclude_none=True)
    )
    if response.status_code == 200:
        user = UserPublic.model_validate_json(response.content)
        return user
    else:
        raise APIException(APIError.model_validate_json(response.content))


def delete_user(user_id: str) -> Message:
    response = openapi.delete(f"/users/{user_id}")
    if response.status_code == 200:
        message = Message.model_validate_json(response.content)
        return message
    else:
        raise APIException(APIError.model_validate_json(response.content))


def read_user_me() -> UserPublic:
    response = openapi.get("/users/me")
    if response.status_code == 200:
        user = UserPublic.model_validate_json(response.content)
        return user
    else:
        raise APIException(APIError.model_validate_json(response.content))


def update_user_me(user: UserUpdateMe) -> UserPublic:
    response = openapi.patch(
        "/users/me", data=user.model_dump_json(exclude_none=True)
    )
    if response.status_code == 200:
        return UserPublic.model_validate_json(response.content)
    else:
        raise APIException(APIError.model_validate_json(response.content))


def delete_user_me() -> Message:
    response = openapi.delete("/users/me")
    if response.status_code == 200:
        return Message.model_validate_json(response.content)
    else:
        raise APIException(APIError.model_validate_json(response.content))


def update_password_me(data: UpdatePassword) -> Message:
    response = openapi.patch(
        "/users/me/password", data=data.model_dump_json(exclude_none=True)
    )
    if response.status_code == 200:
        return Message.model_validate_json(response.content)
    else:
        raise APIException(APIError.model_validate_json(response.content))

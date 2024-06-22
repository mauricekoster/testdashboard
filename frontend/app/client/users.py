from .main import openapi
from app.models import UserCreate, UserPublic, UsersPublic
from . import APIException


def read_users(skip: int = 0, limit: int = 100) -> UsersPublic:
    response = openapi.get(f"/api/v1/users/?skip={skip}&limit={limit}")
    if response.status_code == 200:
        return UsersPublic.model_validate_json(response.content)
    else:
        raise APIException(f'API: {response.json()["detail"]}')


def create_user(userdata: UserCreate) -> UserPublic:
    response = openapi.post("/api/v1/users/", data=userdata.model_dump_json())
    if response.status_code == 200:
        user = UserPublic.model_validate_json(response.content)
        return user
    else:
        raise APIException(f'API: {response.json()["detail"]}')


def read_user_me() -> UserPublic:
    response = openapi.get("/api/v1/users/me")
    if response.status_code == 200:
        user = UserPublic.model_validate_json(response.content)
        return user
    else:
        raise APIException(f'API: {response.json()["detail"]}')

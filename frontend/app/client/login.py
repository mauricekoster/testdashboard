from .main import openapi
from app.models import Token, APIError
from . import APIException


def login_access_token(username, password) -> Token:
    response = openapi.post(
        "/api/v1/login/access-token", data=dict(username=username, password=password)
    )

    if response.status_code == 200:
        token = Token.model_validate_json(response.content)
        return token

    else:
        raise APIException(APIError.model_validate_json(response.content))

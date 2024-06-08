from .main import openapi


def login_access_token(username, password):
    response = openapi.post(
        "/api/v1/login/access-token", data=dict(username=username, password=password)
    )

    if response.status_code == 200:
        return True, response.json()["access_token"]

    else:
        return False, response.json()["detail"]

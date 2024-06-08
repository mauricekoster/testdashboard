from .main import openapi


def read_user_me():
    response = openapi.get("/api/v1/users/me")
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json()["detail"]

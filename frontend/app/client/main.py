import requests
import os
from nicegui import app


class OpenAPI:
    base_url = ""
    token = ""

    def __init__(self):
        self.base_url = os.environ.get("BACKEND_API_URL", "http://localhost")
        if self.base_url.endswith("/"):
            self.base_url.rstrip("/")
        self.token = ""
        self.session = requests.Session()

    def set_header(self):
        if app.storage.user.get("authenticated", False):
            token = app.storage.user.get("access_token")
            self.session.headers["Authorization"] = f"Bearer {token}"
        else:
            if "Authorization" in self.session.headers:
                del self.session.headers["Authorization"]

    def __str__(self) -> str:
        return f"<OpenAPI: baseurl: {self.base_url}>"

    def get(self, url):
        self.set_header()
        print(self.session.headers)
        return self.session.get(f"{self.base_url}{url}")

    def post(self, url, data):
        self.set_header()
        print(f"posting {url}")
        return self.session.post(f"{self.base_url}{url}", data=data)


openapi = OpenAPI()


def clear_token() -> None:
    openapi.set_token("")


def set_token(token: str) -> None:
    openapi.set_token(token)

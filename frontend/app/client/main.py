import requests
import os


class OpenAPI:
    base_url = ""
    token = ""

    def __init__(self):
        self.base_url = os.environ.get("BACKEND_API_URL", "http://localhost")
        if self.base_url.endswith("/"):
            self.base_url.rstrip("/")
        self.token = ""
        self.session = requests.Session()

    def set_token(self, token: str):
        self.token = token
        print("Setting token")
        if self.token:
            self.session.headers["Authorization"] = f"Bearer {self.token}"
        else:
            del self.session.headers["Authorization"]

    def __str__(self) -> str:
        return f"<OpenAPI: baseurl: {self.base_url}>"

    def get(self, url):
        print(self.session.headers)
        return self.session.get(f"{self.base_url}{url}")

    def post(self, url, data):
        print(f"posting {url}")
        return self.session.post(f"{self.base_url}{url}", data=data)


openapi = OpenAPI()


def clear_token() -> None:
    openapi.set_token("")


def set_token(token: str) -> None:
    openapi.set_token(token)

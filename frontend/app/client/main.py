import requests
import os
from nicegui import app

from . import APIException

import logging

log = logging.getLogger('TRS')
logging.basicConfig(level=logging.INFO)


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

    def patch(self, url, data):
        self.set_header()
        print(f"patching {url}")
        return self.session.patch(f"{self.base_url}{url}", data=data)

    def delete(self, url):
        self.set_header()
        print(f"deleting {url}")
        return self.session.delete(f"{self.base_url}{url}")


openapi = OpenAPI()

def get_generic(url):
    response = openapi.get(url)
    if response.status_code == 200:
        result = response.json()
        return result

    else:
        raise APIException(f"get_generic: {response.json()}")


def post_generic(url, data):
    response = openapi.post(url, data=data)
    if response.status_code == 200:
        result = response.json()
        return result

    else:
        raise APIException(f"get_generic: {response.json()}")

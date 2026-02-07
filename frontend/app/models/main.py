from pydantic import BaseModel


class APIError(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    message: str


class ApplicationInfo(BaseModel):
    shortname: str | None = None
    name: str | None = None
    description: str | None = None
    icon: str | None = None

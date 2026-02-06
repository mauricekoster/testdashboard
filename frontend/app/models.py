from pydantic import BaseModel


class APIError(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    message: str


class UserBase(BaseModel):
    email: str
    full_name: str | None
    is_active: bool
    is_superuser: bool


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: str | None  # type: ignore
    password: str | None


class UserPublic(UserBase):
    id: str


class UserUpdateMe(BaseModel):
    full_name: str
    email: str


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int



class ApplicationInfo(BaseModel):
    shortname: str | None = None
    name: str | None = None
    description: str | None = None
    icon: str | None = None

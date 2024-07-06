from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    message: str


class UserBase(BaseModel):
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: str | None  # type: ignore
    password: str | None


class UserPublic(UserBase):
    id: int


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int

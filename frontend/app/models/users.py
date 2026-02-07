from pydantic import BaseModel

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


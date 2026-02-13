import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel


# Properties to return via API, id is always required
class RequirementTypeBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    order: int
    default: bool = False
    buildin: bool = True


# class RequirementType(RequirementTypeBase, table=True):
#     project_id: int | None
#     created_at: datetime | None = None


# API models

class RequirementTypePublic(RequirementTypeBase):
    pass


class RequirementTypesPublic(SQLModel):
    data: list[RequirementTypePublic]


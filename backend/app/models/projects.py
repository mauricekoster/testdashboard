import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)

# Shared properties
class ProjectBase(SQLModel):
    name: str = Field(unique=True, index=True, max_length=100, title="Name", description="Name of project")
    description: str | None = Field(default=None, max_length=10000)
    completed: bool = False


class ProjectCreate(SQLModel):
    name: str
    symbol_id: int
    start_at: str | None = None
    ends_at: str | None = None
    uses_applications: bool = False
    uses_requirements: bool = False
    uses_risks: bool = False
    uses_issues: bool = False
    uses_messages: bool = False


class ProjectUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    start_at: str | None = None
    ends_at: str | None = None
    uses_applications: bool | None = None
    uses_requirements: bool | None = None
    uses_risks: bool | None = None
    uses_issues: bool | None = None
    uses_messages: bool | None = None
    symbol_id: int | None = None
    completed: bool | None = None

# Database model, database table inferred from class name
class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    key: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True)

    description: str | None = None
    symbol_id: int = 0
    start_at: str | None = None
    ends_at: str | None = None
    completed: bool = False
    
    symbol_id: int | None
    # symbol: relation to symbols

    


    uses_applications: bool = False
    uses_requirements: bool = False
    uses_risks: bool = False
    uses_issues: bool = False
    uses_messages: bool = False
    
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    created_by_id: int | None = None
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_by_id: int | None = None
    deleteded_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    deleted_by_id: int | None = None

    # memberships
    # locks

    

# Properties to return via API, id is always required
class ProjectEntryPublic(ProjectBase):
    id: int
    created_at: datetime | None = None


class ProjectPublic(SQLModel):
    data: ProjectEntryPublic

class ProjectsPublic(SQLModel):
    data: list[ProjectEntryPublic]
    count: int

from pydantic import BaseModel, Field
from datetime import datetime



# Shared properties
class ProjectBase(BaseModel):
    name: str
    description: str | None
    completed: bool = False


# Properties to return via API, id is always required
class ProjectEntryPublic(BaseModel):
    name: str = 'noname'
    description: str | None = None
    completed: bool = False
    id: int
    created_at: str

class ProjectCreate(ProjectBase):
    name: str
    symbol_id: int

    start_at: str | None = None
    ends_at: str | None = None
    uses_applications: bool = False
    uses_requirements: bool = False
    uses_risks: bool = False
    uses_issues: bool = False
    uses_messages: bool = False



class ProjectPublic(BaseModel):
    data: ProjectEntryPublic

class ProjectsPublic(BaseModel):
    data: list[ProjectEntryPublic]
    count: int

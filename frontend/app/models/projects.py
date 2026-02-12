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


class ProjectPublic(BaseModel):
    data: ProjectEntryPublic

class ProjectsPublic(BaseModel):
    data: list[ProjectEntryPublic]
    count: int

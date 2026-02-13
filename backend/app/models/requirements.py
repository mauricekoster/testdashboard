from sqlmodel import SQLModel, Field


class RequirementBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    code: str
    name: str
    description: str
    project_id: int
    requirement_type_id: int

class Requirement(RequirementBase, table=True):
    pass


class RequirementPublic(RequirementBase):
    pass

class RequirementsPublic(SQLModel):
    data: list[RequirementPublic]

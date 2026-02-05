from pydantic import BaseModel


class ApplicationInfo(BaseModel):
    shortname: str | None = None
    name: str | None = None
    description: str | None = None
    icon: str | None = None


class ReleaseInfo(BaseModel):
    release: str | None = None
    #locked: bool | None = None
    archived: bool | None = None


class Groups(BaseModel):
    name: str
    groups: list[str]


class GroupInfo(BaseModel):
    groupnames: list[str]
    groupings: list[Groups]

class GroupMatrix(BaseModel):
    group: str | None = None
    row: str
    column: str


class ActiveRelease(BaseModel):
    active_release: str


class LockState(BaseModel):
    locked: bool

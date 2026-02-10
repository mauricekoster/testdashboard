import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.models import (
    Project,
    ProjectCreate,
    ProjectEntryPublic,
    ProjectPublic,
    ProjectsPublic
)

router = APIRouter()




@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProjectPublic,
)
def create_project(session: SessionDep, project_in: ProjectCreate) -> Any:
    """
    Create a project.
    """
 
    project = crud.get_project_by_name(session=session, name=project_in.name)
    if project:
        raise HTTPException(
            status_code=400,
            detail="The project with this name already exists in the system.",
        )

    project = crud.create_project(session=session, project_create=project_in)
    return ProjectPublic(data=project)


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProjectsPublic,
)
def read_projects(session: SessionDep, limit: int = 100, page: int = 1, query: str | None = None) -> Any:
    """
    Retrieve a list of projects.
    """

    count_statement = select(func.count()).select_from(Project)
    count = session.exec(count_statement).one()

    skip = (page - 1) * limit
    statement = (
        select(Project).order_by(col(Project.created_at).desc()).offset(skip).limit(limit)
    )
    projects = session.exec(statement).all()

    return ProjectsPublic(data=projects, count=count)

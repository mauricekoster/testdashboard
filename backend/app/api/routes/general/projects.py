import uuid
from typing import Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
    get_current_user,
)
from app.core.config import settings
from app.models import (
    Project,
    ProjectCreate,
    ProjectUpdate,
    ProjectEntryPublic,
    ProjectPublic,
    ProjectsPublic
)

router = APIRouter()

# TODO: https://testdriven.io/blog/fastapi-jwt-auth/#jwt-authentication



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


@router.get(
    "/{projectId}",
    dependencies=[Depends(get_current_user)],
    response_model=ProjectPublic,
    name="Retrieve a single project"
)
def read_project(projectId: int, session: SessionDep) -> ProjectPublic:
    """
    Retrieve a project using its identifier.
    """
    project = crud.get_project_by_id(session=session, id=projectId)
    return ProjectPublic(data=project)


@router.put(
    "/{projectId}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProjectPublic,
    name="Update a project"
)
def update_project(projectId: int, session: SessionDep, project_in: ProjectUpdate) -> ProjectPublic:
    """
    Update a project using its identifier.
    """
    project = crud.get_project_by_id(session=session, id=projectId)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_dict = project_in.model_dump(exclude_unset=True)
    project.sqlmodel_update(update_dict)
    session.add(project)
    session.commit()
    session.refresh(project)

    return ProjectPublic(data=project)


@router.post(
    "/{projectId}/archive",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProjectPublic,
    name="Archive a project"
)
def archive_project(projectId: int, session: SessionDep, current_user: CurrentUser) -> ProjectPublic:
    """
    Archive a project using its identifier.
    """
    project = crud.get_project_by_id(session=session, id=projectId)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_dict = {
        "deleteded_at": datetime.now(timezone.utc), 
        # "deleted_by_id": current_user.id
        }
    
    project.sqlmodel_update(update_dict)
    session.add(project)
    session.commit()
    session.refresh(project)

    return ProjectPublic(data=project)


@router.post(
    "/{projectId}/unarchive",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProjectPublic,
    name="Unarchive a project"
)
def unarchive_project(projectId: int, session: SessionDep, current_user: CurrentUser) -> ProjectPublic:
    """
    Unarchive a project using its identifier.
    """
    project = crud.get_project_by_id(session=session, id=projectId)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_dict = {
        "deleteded_at": None, 
        # "deleted_by_id": current_user.id
        }
    
    project.sqlmodel_update(update_dict)
    session.add(project)
    session.commit()
    session.refresh(project)

    return ProjectPublic(data=project)
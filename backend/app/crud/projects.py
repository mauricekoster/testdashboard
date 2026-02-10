from typing import Any

from sqlmodel import Session, select


from app.models import Project, ProjectCreate


def create_project(*, session: Session, project_create: ProjectCreate) -> Project:
    db_obj = Project.model_validate(
        project_create, update={
                
            }
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj



def get_project_by_id(*, session: Session, id: int) -> Project | None:
    statement = select(Project).where(Project.id == id)
    session_project = session.exec(statement).first()
    return session_project


def get_project_by_key(*, session: Session, key: str) -> Project | None:
    statement = select(Project).where(Project.key == key)
    session_project = session.exec(statement).first()
    return session_project


def get_project_by_name(*, session: Session, name: str) -> Project | None:
    statement = select(Project).where(Project.name == name)
    session_project = session.exec(statement).first()
    return session_project


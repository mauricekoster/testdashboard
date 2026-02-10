import uuid
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.models import ProjectCreate, ProjectPublic
from app.crud import create_user
from tests.utils.utils import random_email, random_lower_string



def test_create_project_minimal(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> ProjectPublic:
    
    data = {"name": "test_1", "symbol_id": 99}
    r = client.post(
        f"{settings.API_V1_STR}/projects/",
        headers=superuser_token_headers,
        json=data,
    )
    created_project = r.json()
    assert r.status_code == 200


def test_get_projects(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    
    project_in = ProjectCreate(name="test_1", symbol_id=0)
    crud.create_project(session=db, project_create=project_in)

    r = client.get(f"{settings.API_V1_STR}/projects", headers=superuser_token_headers)
    current = r.json()
    assert current


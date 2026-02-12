from .main import openapi
from app.models import (
    APIError,
    ProjectPublic,
    ProjectsPublic,
)
from . import APIException


def read_projects(page: int = 1, limit: int = 100) -> ProjectsPublic:
    response = openapi.get(f"/projects/?page={page}&limit={limit}")
    if response.status_code == 200:
        print(response.content)
        return ProjectsPublic.model_validate_json(response.content, extra='ignore')
        #return response.json()
    else:
        raise APIException(APIError.model_validate_json(response.content))


def read_project(project_id: int) -> ProjectPublic:
    response = openapi.get(f"/projects/{project_id}")
    if response.status_code == 200:
        print(response.content)
        return ProjectPublic.model_validate_json(response.content, extra='ignore')
        #return response.json()
    else:
        raise APIException(APIError.model_validate_json(response.content))


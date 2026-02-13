import uuid
from typing import Any

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
    RequirementTypePublic,
    RequirementTypesPublic
#    RequirementTypeTable
)



router = APIRouter()

@router.get(
    "/{projectId}/requirement-types",
    dependencies=[Depends(get_current_user)],
    response_model=RequirementTypesPublic,
)
def read_requirement_types(
    projectId: int, 
    session: SessionDep, limit: int = 100, page: int = 1) -> RequirementTypesPublic:
    """
    Retrieve a list of requirement types.
    """

    ret = [
        RequirementTypePublic(id=1, name="Business", order=1, default=True),
        RequirementTypePublic(id=2, name="User", order=2),
        RequirementTypePublic(id=3, name="Functional", order=3),
        RequirementTypePublic(id=4, name="Non-functional", order=4),
    ]
    
    return RequirementTypesPublic(data=ret)
    
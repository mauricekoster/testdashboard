import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
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
    RequirementPublic,
    RequirementsPublic
)



router = APIRouter()

@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=RequirementsPublic,
)
def read_requirements(
    session: SessionDep, 
    request: Request,
    limit: int = 100, 
    page: int = 1,
    
    ) -> RequirementsPublic:
    """
    Retrieve a list of requirements.
    """
    print(request.query_params)
    
    source = [
        RequirementPublic(id = 1, code='RQ1', name="Requirement #1", description="Hallo", project_id=1, requirement_type_id=1),
        RequirementPublic(id = 2, code='RQ2', name="Requirement #2", description="Hallo", project_id=1, requirement_type_id=1),
        RequirementPublic(id = 3, code='RQ3', name="Requirement #3", description="Hallo", project_id=1, requirement_type_id=2),
        RequirementPublic(id = 4, code='RQ4', name="Requirement #4", description="Hallo", project_id=1, requirement_type_id=2),
        RequirementPublic(id = 5, code='RQ5', name="Requirement #5", description="Hallo", project_id=1, requirement_type_id=2),
        RequirementPublic(id = 6, code='RQ6', name="Requirement #6", description="Hallo", project_id=1, requirement_type_id=3),
        RequirementPublic(id = 7, code='RQ7', name="Requirement #7", description="Hallo", project_id=1, requirement_type_id=3),
        RequirementPublic(id = 8, code='RQ8', name="Requirement #8", description="Hallo", project_id=1, requirement_type_id=3),
        RequirementPublic(id = 9, code='RQ9', name="Requirement #9", description="Hallo", project_id=1, requirement_type_id=3),
        RequirementPublic(id = 10, code='RQ10', name="Requirement #10", description="Hallo", project_id=1, requirement_type_id=4),
        RequirementPublic(id = 11, code='RQ11', name="Requirement #11", description="Hallo", project_id=1, requirement_type_id=1),
        RequirementPublic(id = 12, code='RQ12', name="Requirement #12", description="Hallo", project_id=1, requirement_type_id=2),

    ]
    print(f"page: {page} limit: {limit}")
    start = (page-1) * limit
    end = start + limit
    ret = source[start:end]

    return RequirementsPublic(data=ret)
    
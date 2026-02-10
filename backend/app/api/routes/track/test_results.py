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
# from app.models import (
  
# )



router = APIRouter()

@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    #response_model=ProjectsPublic,
)
def read_test_results(session: SessionDep, limit: int = 100, page: int = 1, query: str | None = None) -> Any:
    """
    Retrieve a list of test results.
    """

    raise HTTPException(418, "Not Yet Implemented")
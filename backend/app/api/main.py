from fastapi import APIRouter

from app.api.routes import apps, health, login, private, upload, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(private.router, prefix="/private", tags=["private"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(apps.router, prefix="/apps", tags=["apps"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])

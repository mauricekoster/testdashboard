from nicegui import APIRouter

from . import dashboard, admin, projects, login, myprofile, mywork, settings


router = APIRouter()
router.include_router(dashboard.router)
router.include_router(admin.router)
router.include_router(projects.router)
router.include_router(myprofile.router)
router.include_router(mywork.router)
router.include_router(login.router)
router.include_router(settings.router)

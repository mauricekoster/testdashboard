from nicegui import APIRouter

from . import (
    app_pages, app_dashboard, app_releases, 
    dashboard, admin, home_page, 
    project, projects, 
    login, myprofile, mywork, settings,
    chat
)


router = APIRouter()
router.include_router(dashboard.router)
router.include_router(admin.router)
router.include_router(project.router)
router.include_router(projects.router)
router.include_router(myprofile.router)
router.include_router(mywork.router)
router.include_router(login.router)
router.include_router(settings.router)

router.include_router(home_page.router)
router.include_router(app_pages.router)
router.include_router(app_dashboard.router)
router.include_router(app_releases.router)

router.include_router(chat.router)

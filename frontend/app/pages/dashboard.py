from nicegui import ui, APIRouter


router = APIRouter()


@router.page("/")
def show_dashboard():
    ui.navigate.to("/projects")
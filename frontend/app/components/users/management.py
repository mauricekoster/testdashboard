from nicegui import ui
from app.client.users import read_users
from .add import AddUser
from app.components.common import Gravatar

class UserManagement():

    def __init__(self):

        self.current_page = 1
        self.limit = 5

        with ui.row().classes('w-full'):
            ui.space()
            ui.button("Invite User...", color="secundary").classes("outline").props('no-caps')
            ui.button("Add User", on_click=self.on_handle_add).props('no-caps')

            self.overview()

    @ui.refreshable
    def overview(self):

        self.users = read_users(page=self.current_page, limit=self.limit)

        with ui.card().classes("w-full"):
            total_pages = (self.users.count // self.limit) + 1
            with ui.row().classes('w-full'):
                ui.space()
                ui.pagination(
                    min=1, 
                    max=total_pages, 
                    direction_links=True,
                    value=self.current_page, 
                    on_change=self.change_page
                    )
                ui.input(placeholder='Search...', on_change=self.change_search).props('rounded outlined dense debounce=1000').classes('text-xs')
            


            with ui.row().classes('w-full'):
                ui.label("").classes("w-10")
                ui.label("Name").classes("text-bold")

            for user in self.users.data:
                ui.separator()
                with ui.row().classes('w-full'):
                    with ui.column().classes("w-10"):
                        Gravatar(user.email)
                    with ui.column():
                        ui.label(user.full_name).classes('text-bold')
                        ui.label(user.email)

                    ui.space()
                    if user.is_superuser:
                        ui.chip("Admin").props('rounded')
                    ui.button(icon='edit').props('outline')


    def change_search(self, event):
        pass

    def change_page(self, event):
        self.current_page = int(event.value)
        self.overview.refresh()

    async def on_handle_add(self):
        add_dialog = AddUser(self.overview)
        await add_dialog.show()
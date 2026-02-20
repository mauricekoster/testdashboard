from nicegui import ui
from app.client.projects import read_projects
from app.components.common import Icon, Heading, Text
from app.components.project.add import ProjectAdd

class ProjectsManagement():
    def __init__(self):

        self.current_page = 1
        self.limit = 5

        with ui.row().classes('w-full'):
            ui.space()
            ui.button("...", color="secundary").classes("outline")
            ui.button("Create Project", on_click=self.on_handle_add)

        self.overview()
        
            
    @ui.refreshable
    def overview(self):
        self.projects = read_projects(page=self.current_page, limit=self.limit)
        with ui.card().classes("w-full"):
            
            total_pages = (self.projects.count // self.limit) + 1
            with ui.row().classes('w-full'):
                ui.space()
                ui.input(placeholder='Search...', on_change=self.change_search).props('rounded outlined dense debounce=1000').classes('text-xs')
            
            for project in self.projects.data:
                with ui.card().classes('w-full'):
                    with ui.row().classes('w-full p-1'):
                        Icon("o_home", size="3xl")
                        Heading(project.name, size='xs')
                        Text(project.description)
                        ui.space()

                        if project.completed:
                            ui.chip('Completed', icon='star', color='green').props('outline square').classes('text-xs')
                        ui.button(icon='edit').props('rounded outline')

            with ui.row().classes('w-full'):
                ui.space()
                ui.pagination(
                    min=1, 
                    max=total_pages, 
                    direction_links=True,
                    value=self.current_page, 
                    on_change=self.change_page
                    )
                ui.space()

    def change_search(self, event):
        ui.notify(event)

    def change_page(self, event):
        self.current_page = int(event.value)
        self.overview.refresh()


    async def on_handle_add(self):
        add_dialog = ProjectAdd(self.overview)
        await add_dialog.show()
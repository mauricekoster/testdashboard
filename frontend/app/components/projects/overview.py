from nicegui import ui
from app.components.common import Heading, Icon, Text, TabConfig, TabsBuilder
from functools import partial
from app.client.projects import read_projects


class ActiveProjects:
    def __init__(self):

        self.projects = read_projects()

        with ui.row().classes("w-full"):
            for project in self.projects.data:
                with ui.card().classes('border border-gray-200 w-100 p-5'):
                    with ui.row().classes("w-full"):
                        Icon("o_home", size="4xl")
                        
                        Heading(project.name, "sm")
                        ui.space()
                        ui.button(
                            icon="open_in_new", 
                            color="primary", 
                            on_click=partial(ui.navigate.to, f"/project/{project.id}")
                        ).props("outline")

                    with ui.row().classes("w-full"):
                        Text(project.description)

                    # with ui.row().classes("w-full"):
                    #     ui.separator()
                    # with ui.grid(rows=2, columns=2):
                    #     with ui.row().classes("items-center mx-2"):
                    #         ui.icon('o_create', size='sm')
                    #         ui.markdown(f"**{123}** test cases")
                    #     with ui.row().classes("items-center mx-2"):
                    #         ui.icon('o_schedule', size='sm')
                    #         ui.markdown(f"**{123}** test cases")
                    #     with ui.row().classes("items-center mx-2"):
                    #         ui.icon('o_play_arrow', size='sm')
                    #         ui.markdown(f"**{123}** test results")
                    #     with ui.row().classes("items-center mx-2"):
                    #         ui.icon('o_bug_report', size='sm')
                    #         ui.markdown(f"**{123}** issues")

                    

    def navigate(self, txt):
        print(f"navigate to: {txt}")



class ClosedProjects:
    def __init__(self):
        ui.label("Completed projects")


class ProjectsOverview:
    def __init__(self):
        

        projects_tabs = [
            TabConfig(name="active", label="Active", component=ActiveProjects),
            TabConfig(name="completed", label="Completed", component=ClosedProjects),
        ]
        TabsBuilder(projects_tabs)


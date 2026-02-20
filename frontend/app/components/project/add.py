from app.components.common import Dialog
from app.components.common import Form, Input, FormLabel, Flex
from functools import partial
from app.components.common.form import Checkbox

from app.client.mutation import Mutation
from app.client.projects import create_project

from nicegui import ui

from app.models import ProjectCreate


class ProjectAdd():
    def __init__(self, projectlist):
        self.projectlist = projectlist
        self.model = {
            "name": "",
            "description": "",
            "symbol_id": 1,
            "uses_requirements": True,
            "uses_risks": True,
        }

    
    def content(self):
        with Form(self.model) as form:
            with ui.stepper().props('horizontal header-nav').classes('w-full') as stepper:
                with ui.step('Details').props('header-nav'):
                    Input(form, "name", "Name")
                    Input(form, "description", "Description")

                    with ui.stepper_navigation():
                        ui.button('Features >', on_click=stepper.next)

                with ui.step('Features').props('header-nav'):
                    with Flex():
                        Checkbox(form, "uses_requirements", "Use requirements")
                        Checkbox(form, "uses_risks", "Use risks")
                    with ui.stepper_navigation():
                        # ui.button('Next', on_click=stepper.next)
                        ui.button('< Details', on_click=stepper.previous).props('outline')

    async def show(self):
        dialog = Dialog(
            "Add project",
            content=self.content,
            buttons=[
                ("Save", "primary", self._handle_confirm),
                ("Cancel", "secondary", self._handle_cancel),
            ],
        )
        await dialog.show()

    def _handle_confirm(self):
        data = ProjectCreate.model_validate(self.model)
        Mutation(
            mutation_fn=lambda data: create_project(data),
            on_success=lambda: self.projectlist.refresh(),
            on_error=lambda err: ui.notify(
                f"Something went wrong: {err.detail}", type="negative"
            ),
        )(data)

    def _handle_cancel(self):
        pass

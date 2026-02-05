from nicegui import ui

from app.client.apps import get_matrix, set_matrix, get_groups
from app.client import APIException


class ApplicationMatrix:
    def __init__(self, app_id ) -> None:
        self.current_app = app_id
        self.groups = dict(groupnames=[], groupings=[])
        self.matrix = dict(row="", column="") 
        
        ui.label("Make sure the group information is in a saved state. If comboboxes are out of sync, please click 'Reload'")
        self.row_column_controls()

        with ui.row():
            ui.button("Reload", on_click=self.reload).props("outline")
            ui.button("Save", on_click=self.save)

        self.reload()

    @ui.refreshable
    def row_column_controls(self):
        with ui.card().classes('w-100 items-stretch'):
            options = self.groups['groupnames']
            ui.select(label='Row', options=options).bind_value(self.matrix, "row")
            ui.select(label='Column', options=options).bind_value(self.matrix, "column")


    def reload(self):
        app_id = self.current_app
        self.groups = dict(groupnames=[], groupings=[])
        try: 
            g = get_groups(app_id)
            self.groups.update(g)
        except:
            pass

        self.matrix = dict(row="", column="")   
        try: 
            m = get_matrix(app_id)
            self.matrix.update(m)
        except:
            pass

        self.row_column_controls.refresh()

    def save(self):
        try: 
            set_matrix(self.current_app, self.matrix)
            ui.notify('Saved!', type="positive")
        except:
            ui.notify('Something went wrong!', type="negative")
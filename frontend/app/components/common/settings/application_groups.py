from nicegui import ui, events

from dataclasses import dataclass, field
from typing import Callable, List

from app.client.apps import get_groups, set_groups


@dataclass
class GroupName:
    name: str


@dataclass
class GroupnameList:
    on_change: Callable
    items: List[GroupName] = field(default_factory=list)

    def add(self, name: str) -> None:
        idx = len(self.items)
        self.items.append(GroupName(name))
        self.on_change(idx)

    def remove(self, item: GroupName) -> None:
        idx = self.items.index(item)
        self.items.remove(item)
        self.on_change(idx)

    def reset(self) -> None:
        self.items.clear()



class ApplicationGroups:
    def __init__(self, app_id ) -> None:
        self.current_app = app_id

        self.groups = dict(groupnames=[], groupings=[])
        self.groupnames = GroupnameList(on_change=self.groupnames_changed)

        self.data_grouping = dict(component="", index=-1)

        with ui.tabs().props('align=left').classes('w-full') as tabs:
            group_names_tab = ui.tab('Groupnames')
            groups_tab = ui.tab('Groups')
        with ui.tab_panels(tabs, value=group_names_tab).classes('w-full'):
            with ui.tab_panel(group_names_tab):
                self.groupname_tab_ui()
            with ui.tab_panel(groups_tab):
                self.group_list_ui()

        with ui.row():
            ui.button("Reload", on_click=self.reload).props("outline")
            ui.button("Save", on_click=self.save)

        self.reload()
        self.create_add_dialog()
        self.create_edit_dialog()
        self.create_confirm_delete_dialog()

    def create_add_dialog(self):
        with ui.dialog() as self.add_dialog, ui.card():
            ui.label('Add component')
            self.add_dialog_content()

            with ui.row():
                ui.button('Add', on_click=lambda: self.add_dialog.submit('Add'))
                ui.button('Cancel', on_click=lambda: self.add_dialog.submit('Cancel')).props("outline")

    def create_confirm_delete_dialog(self):
        with ui.dialog() as self.delete_dialog, ui.card():
            ui.label('Delete component')

            ui.label("The component group assignments will be permanently deleted after saving.")
            ui.label("If you are sure, please click 'Confirm' to proceed. This action cannot be undone.")
            
            with ui.row():
                ui.button('Confirm', color="warning", on_click=lambda: self.delete_dialog.submit('Confirm'))
                ui.button('Cancel', on_click=lambda: self.delete_dialog.submit('Cancel')).props("outline")

    @ui.refreshable
    def add_dialog_content(self):
        with ui.column():
            ui.input("Component").bind_value(self.data_grouping, "component")
            for g in self.groupnames.items:
                if g.name in self.data_grouping:
                    ui.input(f"{g.name}").bind_value(self.data_grouping, g.name)

    def create_edit_dialog(self):
        with ui.dialog() as self.edit_dialog, ui.card():
            ui.label('Edit component')
            self.edit_dialog_content()

            with ui.row():
                ui.button('Done', on_click=lambda: self.edit_dialog.submit('Done'))
                ui.button('Cancel', on_click=lambda: self.edit_dialog.submit('Cancel')).props("outline")


    @ui.refreshable
    def edit_dialog_content(self):
        with ui.column():
            ui.input("Component").bind_value(self.data_grouping, "component")
            for g in self.groupnames.items:
                if g.name in self.data_grouping:
                    ui.input(f"{g.name}").bind_value(self.data_grouping, g.name)



    async def show_add_dialog(self):
        self.data_grouping = dict(component="")
        for g in self.groupnames.items:
            self.data_grouping[g.name] = ""

        self.add_dialog_content.refresh()
        result = await self.add_dialog
        if result == 'Add':
            gg = []
            for g in self.groupnames.items:
                gg.append(self.data_grouping[g.name])

            d = dict(name=self.data_grouping["component"], groups=gg)
            self.groups['groupings'].append(d)
            self.group_list.refresh() 
            ui.notify(f'Added!')


    

    def reload(self):
        self.loading = True
        self.groupnames.reset()

        try: 
            g = get_groups(self.current_app)
            self.groups.update(g)
        except:
            pass
        
        for gn in self.groups['groupnames']:
            self.groupnames.add(gn)
        self.loading = False

        self.groupnames_ui.refresh()
        self.group_list.refresh()      

        # TODO: matrix reload  


    @ui.refreshable
    def groupname_tab_ui(self):
        with ui.card().classes('w-100 items-stretch'):
            self.groupnames_ui()
            add_input = ui.input('New item').classes('mx-12').mark('new-item')
            add_input.on('keydown.enter', lambda: self.groupnames.add(add_input.value))
            add_input.on('keydown.enter', lambda: add_input.set_value(''))

    def group_list_ui(self):
        with ui.row().classes('w-full'):
            ui.button('Add', on_click=self.show_add_dialog).props("size='sm'")

        self.group_list()

    @ui.refreshable
    def groupnames_ui(self):
        if not self.groupnames.items:
            ui.label('List is empty.').classes('mx-auto')
            return
        
        for item in self.groupnames.items:
            with ui.row().classes('items-center border px-1'):
                
                ui.label(text=item.name).classes('flex-grow')
                ui.button(on_click=lambda item=item: self.groupnames.remove(item), icon='delete').props('flat fab-mini color=grey')


    def groupnames_changed(self, index):
        if not self.loading:
            ui.notify(f"Index changed: {index}")
            l = len(self.groups['groupnames'])
            if index < l:
                self.groups['groupnames'].pop(index)
                for g in self.groups['groupings']:
                    g['groups'].pop(index)
            else:
                self.groups['groupnames'].append(self.groupnames.items[-1].name)
                for g in self.groups['groupings']:
                    g['groups'].append('TBD')

        self.groupnames_ui.refresh()
        self.group_list.refresh()


    @ui.refreshable
    def group_list(self):
        columns = [
            {
                "name": "id",
                "label": "ID",
                "field": "id",
                "classes": "hidden",
                "headerClasses": "hidden",
            },{
                "name": "name",
                "label": "Component name",
                "field": "name",
                "align": "left",
                "sortable": True,
            }]
        
        for idx, c in enumerate(self.groupnames.items):
            columns.append(dict(
                name=f"group-{idx}",
                label = c.name,
                field=f"group-{idx}",
                align="left"
            ))


        columns.append(
            {"name": "actions", "label": "Actions", "field": "actions", "align": "left"}
        )
        #rows = get_user_list()
        rows = []
        for group_index, r in enumerate(self.groups['groupings']):
            d = dict(name=r['name'], id=group_index)
            
            for idx, g in enumerate(r['groups']):
                d[f'group-{idx}'] = g
            rows.append(d)

        table = ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")
        
        table.add_slot(
            "body-cell-actions",
            r"""
            <q-td key="name" :props="props" class="q-pa-md" style="max-width: 250px">
                <q-btn size="sm" round outline icon="more_vert" color="accent">
                <q-menu>
                    <q-list>
                        <q-item clickable v-close-popup
                            @click="$parent.$emit('component_edit', props.row)"
                        >
                            <q-item-section>
                                <q-icon name="edit"/>
                            </q-item-section>
                            <q-item-section>
                                <q-item-label>Edit</q-item-label>
                            </q-item-section>
                        </q-item>

                        <q-item clickable v-close-popup 
                            @click="$parent.$emit('component_delete', props.row)"
                        >
                            <q-item-section>
                                <q-icon name="delete"/>
                            </q-item-section>
                            <q-item-section>
                                <q-item-label>Delete</q-item-label>
                            </q-item-section>
                        </q-item>

                    </q-list>
                </q-menu>
                </q-btn>
            </q-td>
            """,
        )
        table.on("component_edit", self.component_edit)
        table.on("component_delete", self.component_delete)

    async def component_edit(self, e: events.GenericEventArguments):
        comp_idx = int(e.args["id"])
        
        self.data_grouping = dict(component=e.args['name'])
        for index, g in enumerate(self.groupnames.items):
            self.data_grouping[g.name] = e.args[f'group-{index}']

        self.edit_dialog_content.refresh()
        result = await self.edit_dialog
        if result == 'Done':
            gg = []
            for g in self.groupnames.items:
                gg.append(self.data_grouping[g.name])

            d = dict(name=self.data_grouping["component"], groups=gg)
            self.groups['groupings'][comp_idx].update(d)
            self.group_list.refresh() 
            ui.notify(f'Changed!')

    async def component_delete(self, e: events.GenericEventArguments):
        comp_idx = int(e.args["id"])

        result = await self.delete_dialog
        if result == "Confirm":
            print("DELETE")
            self.groups['groupings'].pop(comp_idx)
            self.group_list.refresh() 
            ui.notify(f'Removed!')


    def save(self):
        print(f"SAVE: {self.groups}")

        try: 
            set_groups(app=self.current_app, data=self.groups)
            ui.notify("Saved!", type="positive")
        except:
            ui.notify("Somethinnnnng went wrong!",  type="negative")
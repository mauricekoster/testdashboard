from nicegui import ui, events
from typing import List, Dict
from app.client import APIException

from .template import mainpage
from app.components.main import heading, navbar
from .menus import main_menu

from app.models import UserCreate
from app.client.users import create_user, read_users


def init() -> None:
    @ui.page("/admin")
    def show_dashboard():
        with mainpage("User Management", main_menu, "admin"):
            content()


async def add_user():
    with ui.dialog() as add_user_dialog, ui.card().style("width: 50%;"):
        with ui.card_section().classes("w-full"):
            with ui.row():
                ui.label("Add User").classes("text-h6")
                ui.space()
                ui.button(
                    icon="close",
                    on_click=lambda: add_user_dialog.submit("Cancel"),
                ).props("round flat dense")

        with ui.card_section().classes("w-full"):
            email = ui.input("Email")
            full_name = ui.input("Full name")
            set_password = ui.input("Set password", password=True)
            confirm_password = ui.input(
                "Confirm password",
                password=True,
                validation={
                    "Password not same": lambda value: value == set_password.value
                },
            )
            with ui.row().classes("w-full"):
                is_superuser = ui.checkbox("Is superuser?")
                is_active = ui.checkbox("Is active?", value=True)

        with ui.card_actions().classes("w-full").props("align=right"):
            ui.button("Save", on_click=lambda: add_user_dialog.submit("Save"))
            ui.button(
                "Cancel",
                color="secondary",
                on_click=lambda: add_user_dialog.submit("Cancel"),
            )

    result = await add_user_dialog
    if result == "Cancel":
        return

    data = UserCreate(
        email=email.value,
        full_name=full_name.value,
        password=set_password.value,
        is_active=is_active.value,
        is_superuser=is_superuser.value,
    )
    try:
        _ = create_user(data)
        user_list.refresh()
    except APIException as e:
        ui.notify(f"Error: {e}", color="negative")


def get_user_list() -> List[Dict]:
    try:
        users = read_users()
        return [
            dict(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
            )
            for user in users.data
        ]
    except APIException as e:
        ui.notify(f"Error: {e}", color="negative")
        return []


def user_edit(e: events.GenericEventArguments):
    ui.notify(f"EDIT/id:{e.args['id']}")
    pass


def user_delete(e: events.GenericEventArguments):
    ui.notify(f"DELETE/id:{e.args['id']}")
    pass


@ui.refreshable
def user_list():
    columns = [
        {
            "name": "id",
            "label": "ID",
            "field": "id",
            "classes": "hidden",
            "headerClasses": "hidden",
        },
        {
            "name": "fullname",
            "label": "Full name",
            "field": "full_name",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "email",
            "label": "Email",
            "field": "email",
            "sortable": True,
            "align": "left",
        },
        {
            "name": "role",
            "label": "Role",
            ":field": "row => row.is_superuser ? 'Superuser':'User'",
            "align": "left",
        },
        {"name": "status", "label": "Status", "field": "is_active", "align": "left"},
        {"name": "actions", "label": "Actions", "field": "actions"},
    ]
    rows = get_user_list()
    table = ui.table(columns=columns, rows=rows, row_key="email").classes("w-full")
    table.add_slot(
        "body-cell-status",
        """
        <q-td key="is_active" :props="props">
            <q-badge :color="props.value ? 'green' : 'red'">
            </q-badge>
            {{ props.value ? 'Active': 'Inactive'}}
        </q-td>
        """,
    )
    table.add_slot(
        "body-cell-actions",
        r"""
        <q-td key="name" :props="props" class="q-pa-md" style="max-width: 250px">
            <q-btn size="sm" round outline icon="more_vert" color="accent">
            <q-menu>
                <q-list>
                    <q-item clickable v-close-popup
                        @click="$parent.$emit('user_edit', props.row)"
                    >
                        <q-item-section>
                            <q-icon name="edit"/>
                        </q-item-section>
                        <q-item-section>
                            <q-item-label>Edit</q-item-label>
                        </q-item-section>
                    </q-item>

                    <q-item clickable v-close-popup 
                        @click="$parent.$emit('user_delete', props.row)"
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
    table.on("user_edit", user_edit)
    table.on("user_delete", user_delete)


def content():
    heading("User Management", 4)
    with navbar():
        ui.button("Add User", icon="add_box", on_click=add_user).props("no-caps")
    user_list()

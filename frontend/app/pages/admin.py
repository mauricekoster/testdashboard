from nicegui import ui, APIRouter
from typing import List, Dict
from functools import partial

from app.client import APIException

from app.components.admin.add_user import AddUser
from app.pages.templates.landing import landingpage
from app.components.main import navbar
from app.components.common import Heading

from app.pages.menus import main_menu

from app.client.users import read_users
from .admin_user import user_edit, user_delete

router = APIRouter()


@router.page("/admin")
def show_dashboard():
    with landingpage("admin"):
        content()


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
    table.on("user_edit", partial(user_edit, user_list))
    table.on("user_delete", partial(user_delete, user_list))


def content():
    Heading("User Management")
    with navbar():
        ui.button("Add User", icon="add_box", on_click=on_handle_add).props(
            "outline no-caps"
        )
    user_list()


async def on_handle_add():
    add_user_dialog = AddUser(user_list)
    await add_user_dialog.show()

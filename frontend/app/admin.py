from nicegui import ui, app

from .page_template import mainpage
from .components import heading, navbar


def init() -> None:
    @ui.page("/admin")
    def show_dashboard():
        with mainpage("User Management", "admin"):
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

    print("XXXXXX")
    result = await add_user_dialog
    if result == "Cancel":
        return

    data = dict(
        email=email.value,
        full_name=full_name.value,
        password=set_password.value,
        is_active=is_active.value,
        is_superuser=is_superuser.value,
    )
    ui.notify(f"You chose {result} Email: {email.value}")


@ui.refreshable
def user_list():
    columns = [
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
    rows = [
        {
            "full_name": "Mister Mister",
            "email": "email@example.com",
            "is_superuser": True,
            "is_active": True,
        },
        {
            "full_name": "Some User",
            "email": "nobody@example.com",
            "is_superuser": False,
            "is_active": False,
        },
    ]
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


def content():
    heading("User Management", 4)
    with navbar():
        ui.button("Add User", icon="add_box", on_click=add_user).props("no-caps")
    user_list()

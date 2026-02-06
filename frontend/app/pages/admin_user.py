from nicegui import ui, events

from app.models import UserUpdate
from app.client import APIException
from app.client.users import delete_user, get_user_by_id, update_user

from .dialogs import user_dialog, alert_dialog


async def user_edit(user_list, e: events.GenericEventArguments):
    user_id = e.args["id"]
    user = get_user_by_id(user_id)
    data = UserUpdate(
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        password=None,
    )

    result = await user_dialog("Edit user", data)
    print(data)
    if result == "Cancel":
        return

    if user.email == data.email:
        data.email = None

    if data.password == "":
        data.password = None

    try:
        _ = update_user(user_id, data)
        user_list.refresh()
    except APIException as error:
        ui.notify(f"Error: {error}", color="negative")


async def user_delete(user_list, e: events.GenericEventArguments):
    answer = await alert_dialog(
        "Delete user", "Are you sure? You will not be able to undo this action."
    )

    if answer == "Cancel":
        return

    user_id = int(e.args["id"])
    try:
        message = delete_user(user_id)
        ui.notify(f"{message.message}", type="positive")
    except APIException as error:
        ui.notify(f"{error}", type="negative")

    user_list.refresh()

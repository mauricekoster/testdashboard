from nicegui import ui
from app.components.componentlist import ComponentList
from app.components.common.delete_confirmation import DeleteConfirmation

from app.client.apps import (
    APIException,
    set_active_release,
    get_release_info,
    update_release_info,
    set_release_lock,
    delete_release as del_release,
)

from app.core.user import current_user


class Release:
    def __init__(self, parent, release, query_params = {}) -> None:
        self.parent = parent
        self.current_app = parent.current_app
        self.current_release = release
        self.active_release = parent.active_release
        self.release_info = {}

        self.current_release_info()

        self.component_list = ComponentList(self, query_params)
        
    @ui.refreshable
    def current_release_info(self):
        with ui.card().classes("w-full").tight():
            with ui.card_section():
                ui.label("Current release:")
                ui.label(f"{self.current_release}").classes("text-bold")

            if self.current_release == '' or self.current_release == 'LATEST':
                return

            if 'locked' in self.release_info:
                locked = self.release_info['locked']
            else:
                locked = False
            #print(f"LOCKED: {locked}")

            if 'archived' in self.release_info:
                archived = self.release_info['archived']
            else:
                archived = False
            #print(f"ARCHIVED: {archived}")

            with ui.card_actions().classes('w-full'):
                with ui.row().classes('w-full'):
                    if archived:
                        ui.label('Release is archived')
                        # if current_user.is_admin():
                        ui.space()
                        ui.button('Unarchive', icon='no_encryption', on_click=self.unarchive_release).props("size=sm")
                    elif locked:
                        ui.label('Release is locked')
                        if current_user.is_admin():
                            ui.space()
                            ui.button('Unlock', icon='no_encryption', on_click=self.unlock_release).props("size=sm")
                    else:
                        if self.active_release == self.current_release:
                            ui.button('Set active', color='grey').props("size=sm").disable()
                        else:
                            ui.button('Set active', color='green', on_click=self.set_active_release).props("size=sm")
                            #if current_user.is_admin():
                            ui.space()
                            ui.button('Archive', icon='lock', on_click=self.archive_release).props("size=sm")
                            ui.button("Delete", icon="delete", color='red', on_click=self.delete_release).props("no-caps size=sm")

    def archive_release(self):
        update_release_info(self.current_app, self.current_release, dict(archived=True))
        self.release_info['archived'] = True
        self.current_release_info.refresh()

    def unarchive_release(self):
        update_release_info(self.current_app, self.current_release, dict(archived=False))
        self.release_info['archived'] = False
        self.current_release_info.refresh()

    def lock_release(self):
        lock = set_release_lock(self.current_app, self.current_release, True)
        if lock:
            self.release_info['locked'] = lock
        self.current_release_info.refresh()

    def unlock_release(self):
        lock = set_release_lock(self.current_app, self.current_release, False)
        if not lock:
            self.release_info['locked'] = lock
        self.current_release_info.refresh()

    def set_active_release(self):
        result = set_active_release(self.current_app, release=self.current_release)
        if result == self.current_release:
            self.active_release = self.current_release
        self.current_release_info.refresh()
        self.parent.set_active_release(self.current_release)

    def delete_release_confirmed(self):
        del_release(self.current_app, self.current_release)
        self.current_release = ""
        self.parent.refresh()
        self.current_release_info.refresh()
        self.component_list.update(self.current_release)

    # TODO: Dialog DialogConfirmation memoryleak (claims max. memory)

    #async def delete_release(self):
    #  await DeleteConfirmation(on_confirm=self.delete_release_confirmed).show()

    def delete_release(self):
        self.delete_release_confirmed()

    def update(self, release):
        self.current_release = release

        if release:
            self.release_info = get_release_info(self.current_app, release)

        self.current_release_info.refresh()
        self.component_list.update(self.current_release)



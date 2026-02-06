from nicegui import ui
from app.client import APIException
from app.components.navbar import navbar
from app.components.release import Release


from app.client.apps import (
    get_active_release,
    get_releases,
)


class Releases:
    def __init__(self, app_id, query_params = {} ) -> None:
        self.current_app = app_id
        try:
            self.active_release = get_active_release(self.current_app)
        except APIException:
            self.active_release = None
        self.releases = get_releases(self.current_app)
        self.other_select = None

        self.release_navbar()        

        if 'release' in query_params:
            self.release = Release(self, query_params['release'], query_params)
        else:
            self.release = Release(self, "", query_params)
        
        
    def on_release(self, e):
        self.release.update(e.sender.text)

    def on_release_archived(self, e):
        if self.archived_select.value is not None:
            self.release.update(e.value)
            #self.archived_select.value = None


    @ui.refreshable
    def release_navbar(self):
        releases = [release for release in self.releases 
                    if release['release'] != 'LATEST'
                    and release['release'] != self.active_release

                    ]
        releases.reverse()
        latest_releases = [release for release in self.releases if release['release'] == 'LATEST']
        active_releases = [release for release in self.releases if release['release'] == self.active_release]

        with navbar():
            if len(latest_releases)>0:
                ui.button("LATEST", color="accent", on_click=self.on_release)

            if len(active_releases)>0:
                ui.button(
                    f"{self.active_release}", color="primary", on_click=self.on_release
                )
            
            active_releases = [release for release in releases if not release['archived']]
            active_releases = sorted(active_releases, key=lambda x: x['release'])
            archived_releases = [release['release'] for release in releases if release['archived']]
            archived_releases = sorted(archived_releases)
            print(archived_releases)
            for r in active_releases:
                ui.button(f"{r['release']}", color="secondary", on_click=self.on_release).props('no-caps')

            self.archived_select = ui.select(
                archived_releases, label="Archived releases", on_change=self.on_release_archived
            ).style("width: 200px; padding-left: 10px;").props("q-px-auto")


    def set_active_release(self, release):
      self.active_release = release
      self.release_navbar.refresh()

    def refresh(self):
      self.releases = get_releases(self.current_app)
      self.release_navbar.refresh()


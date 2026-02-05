from nicegui import ui
from app.components.navbar import navbar

from app.client.apps import (
    APIException,
    get_active_release,
    get_releases,
    get_release_results,
    get_matrix
)

from app.core.groups import Group


def result_badge(result):
    if result is not None:
        status = result['result']
        link = result.get('link', '#')
        with ui.column().props("align=center").classes('w-full border p-1'):
            with ui.link(target=link):
                ui.chip(
                    f"{status}",
                    color={
                        "PASS": "green",
                        "FAIL": "red",
                        "UNKNOWN": "grey",
                    }.get(status, "grey"),
                ).props("dense align='center' size='md'").classes('text-bold m-1')
    else:
        ui.label('').classes('border p-1')

class ResultsDashboard:
    def __init__(self, app_id, query_params = {}  ) -> None:
        self.current_app = app_id
        try:
            self.active_release = get_active_release(self.current_app)
        except APIException:
            self.active_release = None

        if 'release' in query_params:
            self.current_release = query_params['release']
        else:
            self.current_release = None

        self.releases = get_releases(self.current_app)
        try:
            self.matrix = get_matrix(self.current_app)
        except APIException:
            self.matrix = None

        self._groups = Group(app_id)

        releases = [release for release in self.releases if not release.get('archived', False) and release['release'] != 'LATEST']
        latest_releases = [release for release in self.releases if release['release'] == 'LATEST']

        with navbar():
            if len(latest_releases)>0:
                ui.button("LATEST", color="accent", on_click=self.on_release)

            for release in releases:
                if self.active_release and self.active_release == release['release']:
                    ui.button(
                    f"{release['release']}", color="primary", on_click=self.on_release
                    )
                else:
                    ui.button(
                    f"{release['release']}", color="secondary", on_click=self.on_release
                    )
            
        self.dashboard()

    def create_matrix(self):

        if self.current_release is None:
            return None

        if self.matrix is None:
            return None

        results = get_release_results(self.current_app, self.current_release)
        print(f"RESULTS: {results}")

        group = self.matrix.get('group', "no-group")
        row = self.matrix['row']
        column = self.matrix['column']

        if group is None or group == "":
            group = 'no-group'

        print(f"M: {row} {column} {group}")

        group_index = self._groups.group_index.get(group, -1)
        row_index = self._groups.group_index[row]
        column_index = self._groups.group_index[column]

        print(f"I: {row_index} {column_index} {group_index}")

        group_names = []
        row_names = []
        col_names = []
        data = {}

        in_group = None
        print(results)
        for k, v in results.items():
            if k in self._groups.groupings:
                if group_index >= 0:
                    in_group = self._groups.groupings[k][group_index]
                in_row = self._groups.groupings[k][row_index]
                in_col = self._groups.groupings[k][column_index]
            else:
                continue

            if in_group is not None:
                if in_group not in group_names:
                    group_names.append(in_group)

            if in_row not in row_names:
                row_names.append(in_row)

            if in_col not in col_names:
                col_names.append(in_col)

            if group_index >= 0:
                if in_group not in data:
                    data[in_group] = {}    

                if in_row not in data[in_group]:    
                    data[in_group][in_row] = {}    

                data[in_group][in_row][in_col] = dict(
                    result=v['status'], 
                    component=v['name'],
                    link=f'/app/{self.current_app}/releases?release={self.current_release}&component={v["name"]}')

            else:
                if in_row not in data:
                    data[in_row] = {}

                data[in_row][in_col] = dict(
                    result=v['status'], 
                    component=v['name'],
                    link=f'/app/{self.current_app}/releases?release={self.current_release}&component={v["name"]}')

        group_names.sort()
        row_names.sort()
        col_names.sort()

        return {
            "groups": group_names,
            "rows": row_names,
            "columns": col_names,
            "data": data
        }

    def create_matrix_fallback(self):
        row_names = []
        col_names = ['Status']
        data = {}

        if self.current_release is None:
            return None

        results = get_release_results(self.current_app, self.current_release)

        for k, v in results.items():
            if k not in row_names:
                row_names.append(k)

            data[k] = {}
            data[k]['Status'] = dict(
                result=v['status'], 
                component=v['name'],
                link=f'/app/{self.current_app}/releases?release={self.current_release}&component={v["name"]}'
                )

        row_names.sort()

        return {
            "groups": [],
            "rows": row_names,
            "columns": col_names,
            "data": data
        }

    def dashboard_no_groups(self, matrix):
        columns_widths = '250px ' + ' '.join(['100px'] * len(matrix['columns']))
        with ui.grid(columns=columns_widths).classes('w-full gap-0'):
            ui.label("").classes('text-bold')
            for c in matrix['columns']:
                ui.label(c).classes('text-bold').props('align=center').classes('border p-1')

            for r in matrix['rows']:
                row = matrix['data'].get(r, None)
                if row is not None:
                    ui.label(r).classes('text-bold').classes('border p-1')
                    for c in matrix['columns']:
                        value = row.get(c, None)
                        result_badge(value)

    def dashboard_with_groups(self, matrix):
        columns_widths = '250px ' + ' '.join(['100px'] * len(matrix['columns']))
        with ui.grid(columns=columns_widths).classes('w-full gap-0'):
            ui.label("").classes('text-bold')
            for c in matrix['columns']:
                ui.label(c).classes('text-bold').props('align=center').classes('border p-1')

            for g in matrix['groups']:
                ui.label(g).classes('col-span-full border p-1 text-bold bg-slate-100')

                for k, v in matrix['data'][g].items():
                    ui.label(k).classes('text').classes('border p-1')
                    for c in matrix['columns']:
                        value = v.get(c, None)
                        result_badge(value)

    @ui.refreshable
    def dashboard(self):
        ui.label(f"Current: {self.current_release}")

        print(f"MATRIX: {self.matrix}")

        if self.matrix:
            matrix = self.create_matrix()
        else:
            matrix = self.create_matrix_fallback()

        if matrix is None:
            return 

        print(matrix)
        if matrix['groups']:
            self.dashboard_with_groups(matrix)
        else:
            self.dashboard_no_groups(matrix)


    def on_release(self, e):
        value = e.sender.text
        self.current_release = value
        self.dashboard.refresh()

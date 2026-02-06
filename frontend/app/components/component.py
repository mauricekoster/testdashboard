from nicegui import ui, events
import os
import datetime
import time
from functools import partial

from app import components
from app.client.main import post_generic


api_base_url = os.environ.get("BACKEND_API_URL", "http://localhost")
base_url = os.environ.get("BACKEND_URL", api_base_url)


class Component:
    def __init__(self, parent, component, query_params = {}) -> None:
        self.parent = parent
        self.component = component
        self.has_open_component = False
        

        expand_component = False
        if 'component' in query_params:
            # print(f"C: {component['name']} - {query_params}")
            expand_component = component['name'] == query_params['component']

        if expand_component:
            self.has_open_component = True
            # print(f"EXPAND: {component['name']}")

        with ui.expansion(value=expand_component).classes("border w-full").props("dense") as expansion:
            with expansion.add_slot("header"):
                with ui.column().classes("w-full gap-0").props('dense'):
                    with ui.row().classes('w-full'):
                        ui.label(f"{component['name']}").classes("text-bold mr-5")
                        self.overall_status()

                    if "elapsedtime" in component["results"]:
                        n= component['results']['elapsedtime']
                        time_format = time.strftime("%Hh%Mm%Ss", time.gmtime(n))
                        ui.label(f"Elapsed: {time_format}").classes("font-light text-xs")

            with ui.card().classes("w-full").tight():
                with ui.card_section().classes("w-full"):
                    with ui.row().classes("w-full"):
                        ui.label("Results:").classes("text-weight-bold mb-5")

                    with ui.row().classes("w-full"):
                        self.show_overall_test_result()
                        ui.space()
                        self.show_tags_test_result()
                        ui.space()
                        self.show_information()

                with ui.card_section().classes("w-full"):
                    self.show_reports()

    def do_scan(self, url, _: events.GenericEventArguments):
        post_generic(url, {})
        self.parent.refresh()

    def overall_status(self):
        c = self.component
        if "results" in c:
            if "status" in c["results"]:
                status = c["results"]["status"]
                ui.chip(
                    f"{status}",
                    color={
                        "PASS": "green",
                        "FAIL": "red",
                        "UNKNOWN": "grey",
                    }.get(status, "grey"),
                ).props("dense size='sm'")
            else:
                ui.chip("UNKNOWN", color="grey").props("dense size='sm'")

        else:
            ui.chip("UNKNOWN", color="grey").props("dense size='sm'")

    def show_information(self):
        component = self.component
        if "info" in component:
            keys = [
                k
                for k, _ in component["info"].items()
                if k not in ["application", "release", "component"]
            ]
            if len(keys) > 0:
                with ui.grid(columns=2).classes("m-1"):
                    ui.label("Information").classes("col-span-full text-weight-bold")

                    for k in keys:
                        v = component["info"][k]
                        ui.label(k).classes("text-weight-medium")
                        ui.label(v)
            else:
                ui.label("No additional information")

    def show_overall_test_result(self):
        component = self.component
        if "results" in component:
            with ui.row().classes('w-full'):
                if "total" in component["results"]:
                    total = component["results"]["total"]
                    if "pass" in total:
                        ui.chip(f"Pass: {total['pass']}", color="green")
                    if "fail" in total:
                        ui.chip(f"Fail: {total['fail']}", color="red")
                    if "skip" in total:
                        if total['skip'] > 0:
                            ui.chip(f"Skipped: {total['skip']}", color="yellow")
            with ui.grid(columns=2):
                if "elapsedtime" in component["results"]:
                    n= component['results']['elapsedtime']
                    time_format = str(datetime.timedelta(seconds = n))
                    ui.label(f"Elapsed time")
                    ui.label(f"{time_format}")
                if "starttime" in component["results"]:
                    ui.label(f"Start time")
                    ui.label(f"{component['results']['starttime'].replace('T', ' ')}")
                if "endtime" in component["results"]:
                    ui.label(f"End time")
                    ui.label(f"{component['results']['endtime'].replace('T', ' ')}")

    def show_tags_test_result(self):
        component = self.component
        if "results" in component:
            if "tags" in component["results"]:
                with ui.grid(columns=2):
                    for tag in component["results"]["tags"]:
                        results = tag["results"]
                        ui.label(tag["name"])
                        with ui.row():
                            ui.chip(f"{results['pass']}", color="green").props(
                                "size=sm"
                            ).classes("mx-0 px-2")
                            ui.chip(f"{results['fail']}", color="red").props(
                                "size=sm"
                            ).classes("mx-0 px-2")
                            if results['skip'] > 0:
                                ui.chip(f"{results['skip']}", color="yellow").props(
                                    "size=sm"
                                ).classes("mx-0 px-2")

    def show_reports(self):
        component = self.component
        with ui.row().classes("w-full"):
            ui.label("Reports:").classes("text-weight-bold mb-3")

        with ui.row().classes("w-full").props("dense"):
            if "reports" in component:
                for k, v in component["reports"].items():
                    self.show_report(k, v)

            else:
                if "report" in component:
                    self.show_report("Report", component["report"])
                if "log" in component:
                    with ui.link(target=f"{base_url}{component['log']}", new_tab=True):
                        ui.button("Log").props(add="size='sm'")
                if "scan" in component:
                    url = component["scan"]
                    ui.button("Scan").props(add="size='sm'").on(
                        "click", partial(self.do_scan, url)
                    )

    def show_report(self, report_name: str, report):
        rnm = report_name.replace("-", " ")
        btn_props = "size='sm'"
        if isinstance(report, list):
            with ui.dropdown_button(rnm, auto_close=True).props(add=btn_props):
                for rpt in report:
                    with ui.link(target=f"{base_url}{rpt['url']}", new_tab=True):
                        ui.label(rpt["name"]).classes("m-1")
        else:
            with ui.link(target=f"{base_url}{report}", new_tab=True):
                ui.button(rnm).props(add=btn_props)

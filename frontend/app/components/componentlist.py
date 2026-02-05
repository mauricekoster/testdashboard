from nicegui import ui
from app.core.groups import Group
from app.components.component import Component

from app.client.apps import (
    APIException,
    get_release_components,
)


class ComponentList:
  def __init__(self, parent, query_params = {}) -> None:
    self.parent = parent
    self.current_app = parent.current_app
    self.current_release = parent.current_release
    self.query_params = query_params

    # print(f"CL: {query_params}")

    self._group = Group(self.current_app)
    self.components = []

    # group
    if self._group.groups:
        with ui.row().classes("w-full"):
            ui.select(
                self._group.groups["groupnames"],
                label="Group by",
                on_change=self.on_select_group,
            ).bind_value(self._group, "group_by").style("width: 100px")
        ui.separator()

    # component list
    self.component_list()

  @ui.refreshable
  def component_list(self):
    if self.current_release is None or self.current_release == '':
      return

    self.components = get_release_components(self.current_app, self.current_release)

    if len(self.components) == 0:
        return

    group_values = self.get_group_values(self.components)
    
    if self._group.groups:
        with ui.row().classes("w-full"):
            with ui.list().props("bordered separator").classes("w-full"):
                group_values.sort()
                for g in group_values:
                    pass_, fail, unknown = self.count_components_results(g, self.components)
                    with ui.expansion(group="grouping").props(
                        "dense header-class='text-bold'"
                    ).classes("w-full") as expansion:

                        with expansion.add_slot('header'):
                          with ui.column().classes("w-full gap-0").props('dense'):
                            ui.label(g).classes("font-semibold")
                            with ui.row().classes("w-full gap-0 items-center"):
                              if pass_ != 0 and fail == 0 and unknown == 0:
                                extra = ["font-semibold", "text-xs", "text-green-600"]
                              else:
                                extra = ["font-light", "text-xs", "text-gray-600"]
                              ui.label(f"Pass: {pass_}").tailwind(*extra)
                              ui.label(" / ").tailwind("font-light", "text-sm", "text-gray-600", "px-1")
                              if fail != 0:
                                extra = ["font-semibold", "text-xs", "text-red-600"]
                              else:
                                extra = ["font-light", "text-xs", "text-gray-600"]
                              ui.label(f"Fail {fail}").tailwind(*extra)
                              
                              ui.label(" / ").tailwind("font-light", "text-sm", "text-gray-600", "px-1")
                              if pass_ == 0 and fail == 0 and unknown != 0:
                                ui.label(f"Unknown: {unknown}").tailwind("font-semibold", "text-xs","text-gray-800")
                              else:
                                ui.label(f"Unknown: {unknown}").tailwind("font-light", "text-xs","text-gray-600")

                        has_opened_components = self.do_components(g, self.components)
                        # print(f"G: {g} - {has_opened_components}")
                        expansion.value = has_opened_components

    else:
        self.do_components(None, self.components)

  def get_group_values(self, components):
    group_values = []
    if self._group.groups:
        for c in components:
            if "groups" in c:
                index = self._group.group_index[self._group.group_by]
                group = c["groups"][index]
                if group not in group_values:
                    group_values.append(group)

        # Add entry for components without group
        group_values.append("(empty)")
    return group_values

  def count_components_results(self, group, components):
    pass_, fail, unknown = 0, 0, 0

    for c in components:
        if "groups" not in c and group is not None:
            if group != "(empty)":
                continue

        if "groups" in c and group is not None:
            group_index = self._group.group_index[self._group.group_by]
            if group != c["groups"][group_index]:
                continue

        if "results" in c:
            if "status" in c["results"]:
                status = c["results"]["status"]
                match status:
                    case "PASS":
                        pass_ = pass_ + 1
                    case "FAIL":
                        fail = fail + 1
                    case _:
                        unknown = unknown + 1

    return pass_, fail, unknown


  def do_components(self, group, components):
    has_opened_components = False
    for c in components:
        if "groups" not in c and group is not None:
            if group != "(empty)":
                continue

        if "groups" in c and group is not None:
            group_index = self._group.group_index[self._group.group_by]
            if group != c["groups"][group_index]:
                continue

        comp_elem = Component(self, c, self.query_params)
        if comp_elem.has_open_component:
          has_opened_components = True

    return has_opened_components


  def on_select_group(self):
    self.refresh()

  def update(self, release):
    self.current_release = release
    self.refresh()

  def refresh(self):
    self.component_list.refresh()


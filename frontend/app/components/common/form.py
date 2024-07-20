from contextlib import contextmanager

from nicegui.element import Element
from .typography import Text
from typing_extensions import Self, Callable
from nicegui import ui


class Form:
    def __init__(self, model=None, on_submit: Callable | None = None) -> None:
        self.model = model
        self.on_submit = on_submit
        self.elements = {}

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        pass

    def get_value(self, name):
        return getattr(self.model, name).value

    def get_values(self):
        d = {}
        for k, v in self.elements.items():
            d[k] = v.value
        return d

    def register(self, name, element: Element):
        self.elements[name] = element
        element.bind_value(self.model, name)
        setattr(self, name, element)

    def validate(self):
        data = {}
        all_valid = True
        for k, v in self.elements.items():
            name = k
            elem = v
            if elem:
                valid = elem.validate()
                print(f"{name} valid: {valid}")
                data[name] = elem.value
            else:
                valid = True
                data[name] = getattr(self.model, name)
            all_valid = all_valid and valid
        return all_valid, data

    def submit(self):
        if self.on_submit:
            all_valid, data = self.validate()
            if all_valid:
                self.on_submit(data)
            else:
                ui.notify("Validation errors!", type="warning")


class FormLabel(Text):
    def __init__(self, label: str, id: str | None = None) -> None:
        super().__init__(label)
        self.label.classes("text-weight-medium")
        if id:
            self.label.props(f"data-id={id}")


class Input:
    def __init__(
        self,
        form: Form,
        id: str,
        placeholder: str | None = None,
        type: str = "text",
        validation: dict | None = None,
    ) -> None:
        passwrd = type == "password"
        form.register(
            id,
            ui.input(placeholder=placeholder, password=passwrd, validation=validation),
        )


class Checkbox:
    def __init__(self, form: Form, id, label: str, default: bool = False):
        form.register(id, ui.checkbox(label, value=default))

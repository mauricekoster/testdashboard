from contextlib import contextmanager
from .typography import Text
from typing_extensions import Self, Callable
from nicegui import ui


class Form:
    def __init__(self, parent, on_submit: Callable | None = None) -> None:
        self.parent = parent
        self.on_submit = on_submit
        self.elements = []

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        pass

    def register(self, name, element=None):
        self.elements.append(dict(name=name, element=element))

    def submit(self):
        if self.on_submit:
            data = {}
            all_valid = True
            for element in self.elements:
                name = element["name"]
                elem = element["element"]
                if elem:
                    valid = elem.validate()
                    data[name] = elem.value
                else:
                    valid = True
                    data[name] = getattr(self.parent, name)
                all_valid = all_valid and valid

            self.on_submit(data)


class FormLabel(Text):
    def __init__(self, label: str, id: str | None = None) -> None:
        super().__init__(label)
        self.label.classes("text-weight-medium")
        if id:
            self.label.props(f"data-id={id}")


class Input:
    def __init__(
        self, form: Form, id: str, placeholder: str | None = None, type: str = "text"
    ) -> None:
        self.form = form
        self.id = id
        self.value = ""
        passwrd = type == "password"
        self.element = ui.input(placeholder=placeholder, password=passwrd).bind_value(
            self, "value"
        )
        form.register(self.id, self.element)

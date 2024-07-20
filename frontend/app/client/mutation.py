from typing_extensions import Callable

from app.client import APIException


class Mutation:
    def __init__(self, mutation_fn: Callable, on_success: Callable, on_error: Callable):
        self.mutation_fn = mutation_fn
        self.on_success = on_success
        self.on_error = on_error

    def __call__(self, *data):
        self.mutate(*data)

    def mutate(self, *data):
        try:
            self.mutation_fn(*data)
            if self.on_success:
                self.on_success()

        except APIException as exp:
            if self.on_error:
                self.on_error(exp.args[0])
            else:
                raise exp

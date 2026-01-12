

from typing import Callable

class Predicate:
    def __init__(self, func: Callable[[dict], bool], description: str = ""):
        self.func = func
        self.description = description

    def evaluate(self, row: dict) -> bool:
        return self.func(row)

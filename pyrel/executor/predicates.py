"""
We add a simple predicate helper
"""
from .predicate import Predicate


def equals(column: str, value):
    p = Predicate(
        func=lambda row: row.get(column) == value,
        description=f"{column} = {value}"
    )
    p.column = column
    p.value = value
    return p

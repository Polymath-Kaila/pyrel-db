# Manages tables only

from .table import Table
from .schema import Schema


class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name: str, schema: Schema):
        if name in self.tables:
            raise ValueError(f"Table '{name}' already exists")

        self.tables[name] = Table(name, schema)

    def get_table(self, name: str) -> Table:
        if name not in self.tables:
            raise ValueError(f"Unknown table '{name}'")

        return self.tables[name]

import json
import os
from pyrel.storage.table import Table
from pyrel.storage.schema import Schema, Column


class Database:
    def __init__(self, path="db.json"):
        self.tables = {}
        self.path = path

        if os.path.exists(self.path):
            self.load()

    def create_table(self, name, schema):
        if name in self.tables:
            raise ValueError(f"Table '{name}' already exists")

        self.tables[name] = Table(name, schema)
        self.save()

    def get_table(self, name):
        if name not in self.tables:
            raise ValueError(f"Unknown table '{name}'")
        return self.tables[name]

    # -------------------------
    # Persistence
    # -------------------------
    def save(self):
        data = {}

        for name, table in self.tables.items():
            data[name] = {
                "schema": [
                    {
                        "name": c.name,
                        "type": "int" if c.dtype is int else "str",
                        "primary_key": c.primary_key,
                    }
                    for c in table.schema.columns
                ],
                "rows": table.rows,
            }

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        with open(self.path) as f:
            data = json.load(f)

        for name, table_data in data.items():
            columns = [
                Column(
                    c["name"],
                    int if c["type"] == "int" else str,
                    primary_key=c["primary_key"],
                )
                for c in table_data["schema"]
            ]

            schema = Schema(columns)
            table = Table(name, schema)
            table.rows = table_data["rows"]

            self.tables[name] = table

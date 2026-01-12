"""
Entites: table
its purpose is to own the actual data, enforce schema + indexes
"""

from .schema import Schema
from .index import Index


class Table:
    def __init__(self, name: str, schema: Schema):
        self.name = name
        self.schema = schema
        self.rows = []
        self.indexes = {}

        # Create indexes for PK and unique columns
        for col in schema.columns:
            if col.primary_key or col.unique:
                self.indexes[col.name] = Index(
                    column=col.name,
                    unique=True
                )

    def insert(self, row: dict):
        self.schema.validate_row(row)

        row_id = len(self.rows)

        # Enforce indexes
        for col_name, index in self.indexes.items():
            index.insert(row.get(col_name), row_id)

        self.rows.append(row)

    def select_all(self):
        return self.rows

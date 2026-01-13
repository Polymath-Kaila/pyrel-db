# pyrel/executor/executor.py

from pyrel.executor.predicates import equals
from pyrel.storage.schema import Schema
from pyrel.storage.database import Database
from pyrel.parser.ast import (
    CreateTable,
    Insert,
    Select,
    Update,
    Delete,
)


class Executor:
    def __init__(self, database: Database):
        self.db = database

    def execute(self, stmt):
        if isinstance(stmt, CreateTable):
            schema = Schema(stmt.columns)
            self.db.create_table(stmt.table_name, schema)
            return "OK"

        if isinstance(stmt, Insert):
            table = self.db.get_table(stmt.table_name)
            row = dict(
                zip(
                    [c.name for c in table.schema.columns],
                    stmt.values,
                )
            )
            table.insert(row)
            return "OK"

        if isinstance(stmt, Select):
            table = self.db.get_table(stmt.table_name)
            if stmt.where:
                col, val = stmt.where
                return table.select_where(equals(col, val))
            return table.select_all()

        if isinstance(stmt, Update):
            table = self.db.get_table(stmt.table_name)
            col, val = stmt.where
            return table.update_where(equals(col, val), stmt.updates)

        if isinstance(stmt, Delete):
            table = self.db.get_table(stmt.table_name)
            col, val = stmt.where
            return table.delete_where(equals(col, val))

        raise ValueError(f"Unsupported statement: {type(stmt).__name__}")

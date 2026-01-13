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
from pyrel.planner.plan_nodes import (
    TableScan,
    IndexScan,
    NestedLoopJoin,
)


class Executor:
    def __init__(self, database: Database):
        self.db = database

    # -------------------------
    # PROJECTION
    # -------------------------
    def _apply_projection(self, rows, columns):
        if columns is None:
            return rows

        projected = []
        for row in rows:
            projected.append({col: row[col] for col in columns})

        return projected

    # -------------------------
    # EXECUTION
    # -------------------------
    def execute(self, stmt):
        # -------------------------
        # AST EXECUTION
        # -------------------------
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
            self.db.save()
            return "OK"

        if isinstance(stmt, Update):
            table = self.db.get_table(stmt.table_name)
            col, val = stmt.where
            count = table.update_where(equals(col, val), stmt.updates)
            self.db.save()
            return count


        if isinstance(stmt, Delete):
            table = self.db.get_table(stmt.table_name)
            col, val = stmt.where
            count = table.delete_where(equals(col, val))
            self.db.save()
            return count

        # -------------------------
        # PLAN EXECUTION
        # -------------------------
        if isinstance(stmt, TableScan):
            table = self.db.get_table(stmt.table_name)
            rows = table.select_all()
            return self._apply_projection(rows, getattr(stmt, "columns", None))

        if isinstance(stmt, IndexScan):
            table = self.db.get_table(stmt.table_name)
            rows = table.select_where(
                equals(stmt.column, stmt.value)
            )
            return self._apply_projection(rows, getattr(stmt, "columns", None))

        if isinstance(stmt, NestedLoopJoin):
            left_rows = self.execute(stmt.left)
            right_rows = self.execute(stmt.right)

            left_table = stmt.left.table_name
            right_table = stmt.right.table_name

            results = []

            for l in left_rows:
                for r in right_rows:
                    if (
                        l[stmt.left_key.split(".")[1]]
                        == r[stmt.right_key.split(".")[1]]
                    ):
                        row = {}

                        # Namespace left table columns
                        for k, v in l.items():
                            row[f"{left_table}.{k}"] = v

                        # Namespace right table columns
                        for k, v in r.items():
                            row[f"{right_table}.{k}"] = v

                        results.append(row)

            return self._apply_projection(
                results, getattr(stmt, "columns", None)
            )

        # -------------------------
        # FALLBACK
        # -------------------------
        raise ValueError(
            f"Unsupported statement: {type(stmt).__name__}"
        )

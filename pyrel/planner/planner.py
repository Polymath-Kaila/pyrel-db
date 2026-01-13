
from pyrel.planner.plan_nodes import (
    TableScan,
    IndexScan,
    NestedLoopJoin,
)
from pyrel.parser.ast import Select
from pyrel.parser.ast import Select, JoinSelect



class Planner:
    def __init__(self, database):
        self.db = database

    def plan(self, stmt):
        if isinstance(stmt, JoinSelect):
            left = TableScan(stmt.table_name)
            right = TableScan(stmt.join["table"])
            return NestedLoopJoin(
                left=left,
                right=right,
                left_key=stmt.join["left_key"],
                right_key=stmt.join["right_key"],
            )
        if isinstance(stmt, Select):
            return self._plan_select(stmt)
        # Other statements execute directly
        return stmt

    def _plan_select(self, stmt):
        # JOIN case
        if hasattr(stmt, "join") and stmt.join is not None:
            left = TableScan(stmt.table_name)
            right = TableScan(stmt.join["table"])

            return NestedLoopJoin(
                left=left,
                right=right,
                left_key=stmt.join["left_key"],
                right_key=stmt.join["right_key"],
            )

        # WHERE + index
        if stmt.where:
            column, value = stmt.where
            table = self.db.get_table(stmt.table_name)

            if column in table.indexes:
                return IndexScan(stmt.table_name, column, value)

        # Fallback
        return TableScan(stmt.table_name)

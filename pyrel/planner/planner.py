
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
    # JOIN case (planner should normally handle JoinSelect earlier,
    # but this keeps the method robust)
        if hasattr(stmt, "join") and stmt.join is not None:
            left = TableScan(
                stmt.table_name,
                columns=None  # projection handled after join
            )
            right = TableScan(
                stmt.join["table"],
                columns=None
            )

            join_plan = NestedLoopJoin(
                left=left,
                right=right,
                left_key=stmt.join["left_key"],
                right_key=stmt.join["right_key"],
            )

        # Attach projection to the join plan
            join_plan.columns = stmt.columns
            return join_plan

    # WHERE + index
        if stmt.where:
            column, value = stmt.where
            table = self.db.get_table(stmt.table_name)

            if column in table.indexes:
                return IndexScan(
                   stmt.table_name,
                   column,
                   value,
                   columns=stmt.columns
                )

    # Fallback: full table scan
        return TableScan(
            stmt.table_name,
            columns=stmt.columns
    )

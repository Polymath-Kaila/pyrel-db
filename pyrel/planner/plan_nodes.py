
class PlanNode:
    pass


class TableScan(PlanNode):
    def __init__(self, table_name):
        self.table_name = table_name


class IndexScan(PlanNode):
    def __init__(self, table_name, column, value):
        self.table_name = table_name
        self.column = column
        self.value = value


class NestedLoopJoin(PlanNode):
    def __init__(self, left, right, left_key, right_key):
        self.left = left
        self.right = right
        self.left_key = left_key
        self.right_key = right_key

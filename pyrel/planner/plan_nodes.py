
class PlanNode:
    pass


class TableScan(PlanNode):
    def __init__(self, table_name, columns=None):
        self.table_name = table_name
        self.columns = columns

class IndexScan(PlanNode):
    def __init__(self, table_name, column, value, columns=None):
        self.table_name = table_name
        self.column = column
        self.value = value
        self.columns = columns


class NestedLoopJoin(PlanNode):
    def __init__(self, left, right, left_key, right_key):
        self.left = left
        self.right = right
        self.left_key = left_key
        self.right_key = right_key

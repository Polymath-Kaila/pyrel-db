
class Statement:
    pass


class CreateTable(Statement):
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns


class Insert(Statement):
    def __init__(self, table_name, values):
        self.table_name = table_name
        self.values = values


class Select(Statement):
    def __init__(self, table_name, where=None):
        self.table_name = table_name
        self.where = where


class Update(Statement):
    def __init__(self, table_name, updates, where=None):
        self.table_name = table_name
        self.updates = updates
        self.where = where


class Delete(Statement):
    def __init__(self, table_name, where=None):
        self.table_name = table_name
        self.where = where

class JoinSelect(Select):
    def __init__(self, table_name, join, where=None):
        super().__init__(table_name, where)
        self.join = join

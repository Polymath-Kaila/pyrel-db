
from .ast import *
from pyrel.storage.schema import Column
from pyrel.parser.ast import JoinSelect


def parse(sql: str) -> Statement:
    sql = sql.strip().rstrip(";")
    tokens = sql.split()

    command = tokens[0].upper()

    if command == "CREATE":
        return _parse_create(tokens, sql)

    if command == "INSERT":
        return _parse_insert(tokens, sql)

    # JOIN MUST COME BEFORE SELECT
    if command == "SELECT" and "JOIN" in tokens:
        return _parse_join(tokens)

    if command == "SELECT":
        return _parse_select(tokens)

    if command == "UPDATE":
        return _parse_update(tokens, sql)

    if command == "DELETE":
        return _parse_delete(tokens)

    raise ValueError("Unsupported SQL statement")


def _parse_create(tokens, sql):
    table_name = tokens[2]

    inside = sql[sql.index("(")+1 : sql.rindex(")")]
    cols = []

    for col_def in inside.split(","):
        parts = col_def.strip().split()
        name = parts[0]
        dtype = int if parts[1].upper() == "INT" else str
        primary = "PRIMARY" in parts
        cols.append(Column(name, dtype, primary_key=primary))

    return CreateTable(table_name, cols)

def _parse_insert(tokens, sql):
    table_name = tokens[2]
    values_str = sql[sql.index("(")+1 : sql.rindex(")")]
    values = []

    for v in values_str.split(","):
        v = v.strip()
        if v.startswith('"'):
            values.append(v.strip('"'))
        else:
            values.append(int(v))

    return Insert(table_name, values)

def _parse_where(tokens):
    col = tokens[-3]
    val = tokens[-1]
    if val.startswith('"'):
        val = val.strip('"')
    else:
        val = int(val)
    return col, val

def _parse_select(tokens):
    table_name = tokens[3]
    where = None
    if "WHERE" in tokens:
        where = _parse_where(tokens)
    return Select(table_name, where)

def _parse_update(tokens, sql):
    table_name = tokens[1]
    set_part = sql.split("SET")[1].split("WHERE")[0]
    key, value = set_part.split("=")
    updates = {key.strip(): value.strip().strip('"')}

    where = None
    if "WHERE" in tokens:
        where = _parse_where(tokens)

    return Update(table_name, updates, where)

def _parse_delete(tokens):
    table_name = tokens[2]
    where = _parse_where(tokens)
    return Delete(table_name, where)

def _parse_join(tokens):
    left_table = tokens[3]
    right_table = tokens[5]

    on_index = tokens.index("ON")
    condition = tokens[on_index + 1]

    left_key, right_key = condition.split("=")

    return JoinSelect(
        table_name=left_table,
        join={
            "table": right_table,
            "left_key": left_key,
            "right_key": right_key,
        },
    )

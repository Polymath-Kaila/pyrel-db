"""
 Entites: Column, Schema
 I define what a table looks like, not the data itself

"""

from typing import Any


class Column:
    def __init__(
        self,
        name: str,
        dtype: type,
        primary_key: bool = False,
        unique: bool = False,
        nullable: bool = True,
    ):
        self.name = name
        self.dtype = dtype
        self.primary_key = primary_key
        self.unique = unique or primary_key
        self.nullable = nullable if not primary_key else False

    def validate(self, value: Any):
        if value is None:
            if not self.nullable:
                raise ValueError(f"Column '{self.name}' cannot be NULL")
            return

        if not isinstance(value, self.dtype):
            raise TypeError(
                f"Column '{self.name}' expects {self.dtype.__name__}, "
                f"got {type(value).__name__}"
            )
class Schema:
    def __init__(self, columns: list[Column]):
        self.columns = columns
        self.column_map = {col.name: col for col in columns}

        self.primary_keys = [c.name for c in columns if c.primary_key]

        if len(self.primary_keys) > 1:
            raise ValueError("Composite primary keys not supported (yet)")

    def validate_row(self, row: dict):
        for col in self.columns:
            if col.name not in row:
                if not col.nullable:
                    raise ValueError(f"Missing value for column '{col.name}'")
                continue

            col.validate(row[col.name])

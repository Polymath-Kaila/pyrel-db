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

    # Index aware selection
    def _row_matches(self, row_id: int, Predicate):
        row = self.rows[row_id]
        return Predicate.evaluate(row)

    def select_where(self, predicate, use_index: bool = True):
    # Try index-based path
     if use_index and hasattr(predicate, "column") and predicate.column in self.indexes:
        index = self.indexes[predicate.column]
        row_ids = index.lookup(predicate.value)
        return [self.rows[rid] for rid in row_ids if predicate.evaluate(self.rows[rid])]

    # Fallback: full table scan
     return [row for row in self.rows if predicate.evaluate(row)]

    # Update operation
    def update_where(self, predicate, updates: dict):
        updated = 0

        for row_id, row in enumerate(self.rows):
            if predicate.evaluate(row):
               # Remove old index entries
               for col, index in self.indexes.items():
                   index.delete(row.get(col), row_id)

               # Apply updates
               for key, value in updates.items():
                   row[key] = value

               # Validate updated row
               self.schema.validate_row(row)

               # Reinsert into indexes
               for col, index in self.indexes.items():
                   index.insert(row.get(col), row_id)

               updated += 1

    return updated

    # Delete operation
    def delete_where(self, predicate):
        deleted = 0

        new_rows = []
        old_to_new_ids = {}

        for old_id, row in enumerate(self.rows):
            if predicate.evaluate(row):
               deleted += 1
               continue
            new_id = len(new_rows)
            new_rows.append(row)
            old_to_new_ids[old_id] = new_id

    # Rebuild indexes
        self.rows = new_rows
        for index in self.indexes.values():
            index.map.clear()

        for row_id, row in enumerate(self.rows):
            for col, index in self.indexes.items():
                index.insert(row.get(col), row_id)

    return deleted

"""
Entity: Table

Purpose:
- Owns actual row data
- Enforces schema constraints
- Maintains and updates indexes
- Provides basic data operations (insert, select, update, delete)

Design philosophy:
- Simplicity over optimization
- Correctness over performance
- Explicit state management
"""

from .schema import Schema
from .index import Index


class Table:
    def __init__(self, name: str, schema: Schema):
        self.name = name
        self.schema = schema
        self.rows: list[dict] = []
        self.indexes: dict[str, Index] = {}

        # Automatically create indexes for primary key and unique columns
        for column in schema.columns:
            if column.primary_key or column.unique:
                self.indexes[column.name] = Index(
                    column=column.name,
                    unique=True
                )

    # INSERT
    
    def insert(self, row: dict):
        """
        Insert a new row into the table after schema validation
        and index constraint enforcement.
        """
        self.schema.validate_row(row)

        row_id = len(self.rows)

        # Enforce index constraints
        for column_name, index in self.indexes.items():
            index.insert(row.get(column_name), row_id)

        self.rows.append(row)

    # SELECT
   
    def select_all(self):
        """Return all rows in the table."""
        return self.rows

    def select_where(self, predicate, use_index: bool = True):
        """
        Select rows matching a predicate.
        Uses index-based lookup when possible, otherwise falls back to full scan.
        """
        # Index-aware execution path
        if (
            use_index
            and hasattr(predicate, "column")
            and predicate.column in self.indexes
        ):
            index = self.indexes[predicate.column]
            row_ids = index.lookup(predicate.value)
            return [
                self.rows[row_id]
                for row_id in row_ids
                if predicate.evaluate(self.rows[row_id])
            ]

        # Full table scan fallback
        return [row for row in self.rows if predicate.evaluate(row)]

    # UPDATE
   
    def update_where(self, predicate, updates: dict) -> int:
        """
        Update rows matching a predicate.
        Returns the number of updated rows.
        """
        updated = 0

        for row_id, row in enumerate(self.rows):
            if not predicate.evaluate(row):
                continue

            # Remove old index entries
            for column, index in self.indexes.items():
                index.delete(row.get(column), row_id)

            # Apply updates
            for key, value in updates.items():
                row[key] = value

            # Re-validate row after mutation
            self.schema.validate_row(row)

            # Reinsert into indexes
            for column, index in self.indexes.items():
                index.insert(row.get(column), row_id)

            updated += 1

        return updated

    # DELETE
    
    def delete_where(self, predicate) -> int:
        """
        Delete rows matching a predicate.
        Rebuilds storage and indexes.
        Returns the number of deleted rows.
        """
        deleted = 0
        new_rows = []

        for row in self.rows:
            if predicate.evaluate(row):
                deleted += 1
            else:
                new_rows.append(row)

        # Replace rows
        self.rows = new_rows

        # Rebuild indexes from scratch
        for index in self.indexes.values():
            index.map.clear()

        for row_id, row in enumerate(self.rows):
            for column, index in self.indexes.items():
                index.insert(row.get(column), row_id)

        return deleted

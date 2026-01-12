# Schema & Column – Design Notes (Concise)

This document explains the **Schema** and **Column** system at a high level.
This layer defines **structure and rules**, not data storage.

---

## Big Picture

This code does **not store data**.

It defines:

* What a table looks like
* What values are allowed
* What constraints must always hold

Every row must be validated by the schema *before* insertion.

---

## Core Data Model

### Row

A row is represented as a Python dictionary:

```python
{"id": 1, "name": "Alice", "age": 20}
```

The schema decides whether this row is **valid or invalid**.

---

## Column

### Purpose

A `Column` defines **rules for a single field** in a table.

SQL analogy:

```sql
id INT PRIMARY KEY
```

Python metadata:

```python
Column("id", int, primary_key=True)
```

A column:

* Defines a name and data type
* Enforces constraints (PK, unique, nullable)
* Validates a single value

It **never stores data**.

---

### Critical Rules

**Primary keys are always unique and non-null**:

```python
self.unique = unique or primary_key
self.nullable = False if primary_key else nullable
```

These rules are enforced automatically to prevent invalid schemas.

---

### Column Validation Logic

```python
def validate(value):
```

Validation happens in two steps:

1. **NULL check** → reject `None` if not nullable
2. **Type check** → enforce `isinstance(value, dtype)`

This guarantees type safety and predictable rows.

---

## Schema

### Purpose

A `Schema` defines the **structure of a table**.

```text
Table = Columns + Constraints
```

It:

* Groups columns
* Enforces table-level rules
* Validates entire rows

---

### Hash-Based Column Lookup

```python
self.column_map = {col.name: col}
```

Why this matters:

* O(1) column access
* Simple and fast
* Ideal for in-memory databases

---

### Primary Key Handling

```python
self.primary_keys = [c.name for c in columns if c.primary_key]
```

* Used for identity and indexing
* Composite keys are intentionally **not supported** to keep the system minimal

---

## Row Validation

```python
validate_row(row: dict)
```

Validation is **schema-driven**, not user-driven:

* Missing non-nullable columns → error
* Each value is validated by its column

This ensures schema rules always control the data.

---

## Design Philosophy

### Hash-Based Indexing

* O(1) lookups
* Simple implementation
* No ordering or range queries

### Row IDs Instead of Rows

* Avoid duplication
* Lightweight indexes
* Rows can be mutated safely

### Known Limitations (By Design)

* No range queries
* No ordered traversal

These trade-offs keep the RDBMS **small, fast, and understandable**.

---

## Mental Model

* **Column** → rules for one value
* **Schema** → rules for a row
* **Row** → raw data
* **Index** → fast access, not storage

This mirrors the internal structure of real relational databases.

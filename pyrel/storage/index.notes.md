# Index Design Notes

## Why hash-based index?
- O(1) lookups
- Simple to implement
- Good enough for in-memory DB

## Why store row_ids instead of rows?
- Avoids duplication
- Keeps index lightweight
- Allows row mutation

## Limitations
- No range queries
- No ordered traversal

These trade-offs are acceptable for a minimal RDBMS.

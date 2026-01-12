# Table Design Notes

## Why rows as list[dict]?
- Simple mental model
- Easy iteration
- Clear mapping column → value

## Why row_id = index in list?
- Fast
- Stable for lifetime of row
- Easy indexing

## Missing features (future work)
- DELETE
- UPDATE
- WHERE filtering
- JOIN support

## Filtering

Filtering supports:
- index-based lookup when possible
- full scan fallback otherwise

## Deletion Strategy

Rows are physically removed and indexes rebuilt.

Rationale:
- Simplicity
- Correctness
- No tombstones or fragmentation

Trade-off: O(n) delete cost (acceptable for scope).
This mirrors real DB execution strategies at a small scale.
Table is intentionally minimal at this stage.


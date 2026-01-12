# Schema Design Notes

## Why explicit Column objects?
- Makes constraints visible and enforceable
- Avoids implicit assumptions
- Easier to extend (foreign keys, defaults)

## Why Python types for data types?
- Simple and readable
- Explicit trade-off: not SQL-accurate, but intentional
- Shows focus on correctness over completeness

## Limitations (intentional)
- No composite primary keys
- No foreign keys
- No default values

These are consciously omitted to keep the system small and understandable.

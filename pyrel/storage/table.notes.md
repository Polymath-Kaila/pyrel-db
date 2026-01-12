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

Table is intentionally minimal at this stage.

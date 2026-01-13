# AST Design Notes

AST nodes represent *intent*, not execution.

They are:
- immutable
- declarative
- free of storage concerns

Execution happens later in the executor layer.

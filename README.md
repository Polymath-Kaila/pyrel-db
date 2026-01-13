# RDBMS  Project
This project is developed incrementally, starting from a minimal
in-memory storage engine before layering query parsing and execution.

Done in refrence to pesapal's company  idea to challenge junior devs to not only write code but think in systems design, architecture and thinking.  

Carefully and precisely designed and developed by **polymath kaila**

---

## Pipeline
SQL
 - Parser (specific grammar first)
 - AST (JoinSelect vs Select)
 - Planner (AST → PlanNode)
 - Executor (PlanNode execution)
 - Storage

---

## Query Planning
Queries are parsed into an `AST`(Abstract Syntax Tree) and then converted into explicit
execution plans. 
JOIN queries are planned as nested-loop joins,
while simple SELECT queries use index scans when available or
fallback to table scans.

This separation mirrors real relational database engines.

---

## Demo

```text
$ python -m pyrel.repl.repl
db> CREATE TABLE users (id INT PRIMARY KEY, name TEXT);
OK
db> INSERT INTO users VALUES (1, "Alice");
OK
db> SELECT * FROM users WHERE id = 1;
[{'id': 1, 'name': 'Alice'}]
```
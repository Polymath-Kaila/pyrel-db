# RDBMS  Project
This project is developed incrementally, starting from a minimal
in-memory storage engine before layering query parsing and execution.

Done in refrence to pesapal's company  idea to challenge junior devs to not only write code but think in systems design, architecture and thinking.  

Carefully and precisely designed and developed by **polymath kaila**

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
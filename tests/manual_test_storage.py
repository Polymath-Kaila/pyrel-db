from pyrel.storage.schema import Column, Schema
from pyrel.storage.database import Database
from pyrel.executor.predicates import equals

db = Database()

schema = Schema([
    Column("id", int, primary_key=True),
    Column("name", str, nullable=False),
])

db.create_table("users", schema)
users = db.get_table("users")

users.insert({"id": 1, "name": "Alice"})
users.insert({"id": 2, "name": "Bob"})
users.insert({"id": 3, "name": "Charlie"})

print("Select:", users.select_where(equals("id", 2)))
print("Updated:", users.update_where(equals("name", "Alice"), {"name": "Alicia"}))
print("Deleted:", users.delete_where(equals("id", 3)))
print("Final:", users.select_all())

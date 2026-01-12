from pyrel.storage.schema import Column, Schema
from pyrel.storage.database import Database

db = Database()

schema = Schema([
    Column("id", int, primary_key=True),
    Column("name", str, nullable=False),
])

db.create_table("users", schema)

users = db.get_table("users")

users.insert({"id": 1, "name": "Alice"})
users.insert({"id": 2, "name": "Bob"})

print(users.select_all())

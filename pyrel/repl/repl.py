
from pyrel.parser.parser import parse
from pyrel.executor.executor import Executor
from pyrel.storage.database import Database


def start_repl():
    db = Database()
    executor = Executor(db)

    print("PyRelDB — minimal relational database")
    print("Type 'exit' to quit\n")

    while True:
        try:
            sql = input("db> ").strip()
            if sql.lower() in ("exit", "quit"):
                break

            stmt = parse(sql)
            result = executor.execute(stmt)

            if result is not None:
                print(result)

        except Exception as e:
            print(f"Error: {e}")

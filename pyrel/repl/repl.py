
from pyrel.parser.parser import parse
from pyrel.executor.executor import Executor
from pyrel.storage.database import Database
from pyrel.planner.planner import Planner



def start_repl():
    db = Database()
    executor = Executor(db)
    planner = Planner(db)

    print("PyRelDB minimal relational database by polymath")
    print("Type 'exit' to quit\n")

    while True:
        try:
            sql = input("db> ").strip()
            if sql.lower() in ("exit", "quit"):
                break

            stmt = parse(sql)
            plan = planner.plan(stmt)
            result = executor.execute(plan)

            if result is not None:
                print(result)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    start_repl()

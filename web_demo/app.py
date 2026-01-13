from flask import Flask, request, jsonify, render_template
from pyrel.storage.database import Database
from pyrel.executor.executor import Executor
from pyrel.planner.planner import Planner
from pyrel.parser.parser import parse

app = Flask(__name__)

# Single in-memory DB instance
db = Database()
executor = Executor(db)
planner = Planner(db)


def run_sql(sql: str):
    stmt = parse(sql)
    plan = planner.plan(stmt)
    return executor.execute(plan)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/init", methods=["POST"])
def init_db():
    try:
        run_sql("CREATE TABLE users (id INT PRIMARY KEY, name TEXT);")
        return jsonify({"status": "initialized"})
    except ValueError as e:
        return jsonify({
            "status": "already_initialized",
            "message": str(e)
        })



@app.route("/users", methods=["GET"])
def list_users():
    result = run_sql("SELECT * FROM users;")
    return jsonify(result)


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    sql = f'INSERT INTO users VALUES ({data["id"]}, "{data["name"]}");'
    run_sql(sql)
    return jsonify({"status": "created"})


if __name__ == "__main__":
    app.run(debug=True)

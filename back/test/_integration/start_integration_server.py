import sqlite3
import sys
from flask import request

sys.path.append(".")
from config import config


# Crea una base de datos en memoria con las instrucciones
# y modifica el valor de config['database'] con esa base de datos

conn = sqlite3.connect(":memory:", check_same_thread=False)
config["database"] = conn

from src.web.app import app


@app.route("/__testing__/sql", methods=["POST"])
def testing_sql():
    data = request.get_json()
    conn.executescript(data)
    return "", 200


app.run("0.0.0.0", debug=True)

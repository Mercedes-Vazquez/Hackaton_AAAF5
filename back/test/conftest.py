import pytest  # type: ignore
import sqlite3
from src.domain.model.user import hash_password


@pytest.fixture
def database():
    conn = sqlite3.connect(":memory:")
    conn.executescript(
        f"""
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            id varchar primary key,
            username varchar,
            name varchar,
            password varchar,
            is_admin boolean
        );

        DROP TABLE IF EXISTS goals;
        CREATE TABLE IF NOT EXISTS goals (
            id varchar,
            title varchar,
            category varchar,
            status varchar,
            user_id varchar,
            PRIMARY KEY(id),
            FOREIGN KEY ("user_id") REFERENCES users("user_id")
        );

        DROP TABLE IF EXISTS tasks;
        CREATE TABLE IF NOT EXISTS tasks (
            id varchar,
            title varchar,
            description varchar,
            hint varchar,
            goal_id varchar,
            PRIMARY KEY(id),
            FOREIGN KEY ("goal_id") REFERENCES goals("goal_id")
        );

        DROP TABLE IF EXISTS log;
        CREATE TABLE IF NOT EXISTS log (
            timestamp varchar,
            user_id varchar,
            FOREIGN KEY ("user_id") REFERENCES users("user_id")
        );

        INSERT INTO users (id, username, name, password, is_admin) values 
            ("user-1", "user-1@example.com", "User 1", '{hash_password("user-1-password")}', 1),
            ("user-2", "user-2@example.com", "User 2", '{hash_password("user-2-password")}', 0),
            ("user-3", "user-3@example.com", "User 3", '{hash_password("user-3-password")}', 0),
            ("user-4", "user-4@example.com", "User 4", '{hash_password("user-4-password")}', 0);
        """
    )
    return conn

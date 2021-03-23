BEGIN TRANSACTION;

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
    date varchar,
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

DROP TABLE IF EXISTS logs;
CREATE TABLE IF NOT EXISTS logs (
    timestamp varchar,
    user_id varchar,
    FOREIGN KEY ("user_id") REFERENCES users("user_id")
);

DROP TABLE IF EXISTS admin_users;
CREATE TABLE IF NOT EXISTS admin_users (
    admin_id varchar,
    user_id varchar,
    FOREIGN KEY ("admin_id") REFERENCES users("user_id"),
    FOREIGN KEY ("user_id") REFERENCES users("user_id")
);

COMMIT;
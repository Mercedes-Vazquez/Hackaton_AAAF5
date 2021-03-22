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
    title varchar,
    category varchar,
    status varchar,
    user_id varchar,
    PRIMARY KEY(id),
    FOREIGN KEY ("user_id") REFERENCES users("user_id")
);

COMMIT;
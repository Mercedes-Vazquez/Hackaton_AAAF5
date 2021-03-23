BEGIN TRANSACTION;

DELETE FROM users;
INSERT INTO users VALUES 
    ("user-1", "user-1@example.com", "User 1", '{hash_password[user-1-password]}', 0),
    ("user-2", "user-2@example.com", "User 2", '{hash_password[user-2-passwor]}', 0),
    ("user-3", "user-3@example.com", "User 3", '{hash_password[user-3-password]}', 0),
    ("admin-1", "admin-1@example.com", "Admin-1", '{hash_password[admin-1-password]}', 1);

DELETE FROM goals;
INSERT INTO goals VALUES 
    ("test-id-1", "test-date", "test-title", "test-category-1", "test-status", "user-1"),
    ("test-id-2", "test-date", "test-title", "test-category-1", "test-status", "user-1"),
    ("test-id-3", "test-date", "test-title", "test-category-2", "test-status", "user-1"),
    ("test-id-4", "test-date", "test-title", "test-category-2", "test-status", "user-2");

DELETE FROM tasks;
INSERT INTO tasks VALUES
    ("test-id-1", "test-title", "test-description", "test-hint", "test-goal-id-1"),
    ("test-id-2", "test-title", "test-description", "test-hint", "test-goal-id-1");

DELETE FROM logs;
INSERT INTO logs VALUES
    ("2021-03-04T08:47:19Z", "user-1"),
    ("2021-03-04T08:50:23Z", "user-1"),
    ("2021-03-05T08:50:23Z", "user-1"),
    ("2021-03-06T08:50:23Z", "user-1"),
    ("2021-03-06T08:50:23Z", "user-2");

DELETE FROM admin_users;
INSERT INTO admin_users VALUES
    ("admin-1", "user-1"),
    ("admin-1", "user-2"),
    ("admin-1", "user-3");

COMMIT;
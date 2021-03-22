BEGIN TRANSACTION;

DELETE FROM users;
INSERT INTO users VALUES 
    ("user-1", "user-1@example.com", "User 1", '{hash_password["user-1-password"]}', 0),
    ("user-2", "user-2@example.com", "User 2", '{hash_password["user-2-password"]}', 0),
    ("user-3", "user-3@example.com", "User 3", '{hash_password["user-3-password"]}', 0),
    ("user-4", "user-4@example.com", "User 4", '{hash_password["user-4-password"]}', 1);

DELETE FROM goals;
INSERT INTO goals VALUES 
    ("test-id-1", "test-title", "test-category", "test-status", "user-1"),
    ("test-id-2", "test-title", "test-category", "test-status", "user-1"),
    ("test-id-3", "test-title", "test-category", "test-status", "user-1"),
    ("test-id-4", "test-title", "test-category", "test-status", "user-2");

COMMIT;
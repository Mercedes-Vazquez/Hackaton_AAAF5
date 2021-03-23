import sha256 from "js-sha256";
import authStore from "@/stores/auth.js";

beforeEach(async () => {
  authStore.logout();
  const sql = `
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id varchar primary key,
        username varchar,
        name varchar,
        password varchar,
        is_admin boolean
    );
    DROP TABLE IF EXISTS logs;
    CREATE TABLE IF NOT EXISTS logs (
        timestamp varchar,
        user_id varchar,
        FOREIGN KEY ("user_id") REFERENCES users("user_id")
    );
    INSERT INTO users ( id, username, name, password, is_admin) values 
        ("user-1", "user-1@example.com", "User 1", '${sha256(
          "user-1-password"
        )}', 1),
        ("user-2", "user-2@example.com", "User 2", '${sha256(
          "user-2-password"
        )}', 0),
        ("user-3", "user-3@example.com", "User 3", '${sha256(
          "user-3-password"
        )}', 0),
        ("user-4", "user-4@example.com", "User 4", '${sha256(
          "user-4-password"
        )}', 0);
    INSERT INTO logs VALUES
      ("2021-03-04T08:47:19Z", "user-1"),
      ("2021-03-04T08:50:23Z", "user-1"),
      ("2021-03-05T08:50:23Z", "user-1"),
      ("2021-03-06T08:50:23Z", "user-1"),
      ("2021-03-06T08:50:23Z", "user-2");
  `;

  await api.post("/__testing__/sql", sql);
});

test("get routine accomplisment when the user is logged in", async () => {
  expect(api.authToken).toBe(null);
  await authStore.login({
    username: "user-1@example.com",
    password: "user-1-password",
  });
  expect(api.status).toBe(200);
  const frequency = await api.getRoutineAccomplishment();
  expect(frequency.length).toBe(3);
  expect(frequency[0]).toBe("2021-03-04");
});

test("get routine accomplisment when the user is not logged in", async () => {
  expect(api.authToken).toBe(null);
  await api.getRoutineAccomplishment();
  expect(api.status).toBe(401);
});

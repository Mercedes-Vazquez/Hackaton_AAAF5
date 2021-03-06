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
  `;

  await api.post("/__testing__/sql", sql);
});

test("login existent user", async () => {
  expect(api.authToken).toBe(null);
  await authStore.login({
    username: "user-1@example.com",
    password: "user-1-password",
  });

  expect(api.status).toBe(200);
  expect(api.authToken).not.toBe(null);
  expect(authStore.isUserLogged).toBe(true);
  expect(authStore.user).toEqual({
    id: "user-1",
    name: "User 1",
    username: "user-1@example.com",
    is_admin: true,
  });
});

test("login not existent user", async () => {
  expect(api.authToken).toBe(null);
  await authStore.login({
    username: "user-not-exists@example.com",
    password: "user-1-password",
  });
  expect(api.status).toBe(401);
  expect(api.authToken).toBe(null);
  expect(authStore.user).toEqual({});
  expect(authStore.isUserLogged).toBe(false);
});

test("login incorrect password", async () => {
  expect(api.authToken).toBe(null);
  await authStore.login({
    username: "user-1@example.com",
    password: "user-1-bad-password",
  });
  expect(api.status).toBe(401);
  expect(api.authToken).toBe(null);
  expect(authStore.user).toEqual({});
  expect(authStore.isUserLogged).toBe(false);
});

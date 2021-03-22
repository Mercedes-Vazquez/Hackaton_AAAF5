import md5 from "js-md5";
import Vue from "vue";
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
        ("user-1", "user-1@example.com", "User 1", '${md5(
          "user-1-password"
        )}', 1),
        ("user-2", "user-2@example.com", "User 2", '${md5(
          "user-2-password"
        )}', 0),
        ("user-3", "user-3@example.com", "User 3", '${md5(
          "user-3-password"
        )}', 0),
        ("user-4", "user-4@example.com", "User 4", '${md5(
          "user-4-password"
        )}', 0);
  `;

  // /__testing__/sql es un endpoint especial de nuestro backend
  // que nos permite ejecutar instrucciones SQL directamente
  // en la base de datos del backend.
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

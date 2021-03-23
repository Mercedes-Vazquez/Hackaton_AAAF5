export const routes = [
  {
    path: "/",
    component: () => import("@/views/Login/LoginPage.vue"),
  },
  {
    path: "/home",
    component: () => import("@/views/TaskList/TaskListPage.vue"),
  },
  {
    path: "/goal/:id",
    component: () => import("@/views/TaskDetails/TaskDetailsPage.vue"),
  },
  // {
  //   path: "/tasks",
  //   component: () => import("@/views/TaskList/TaskListPage.vue"),
  // },
];

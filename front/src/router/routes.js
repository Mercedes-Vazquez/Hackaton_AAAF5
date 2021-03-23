export const routes = [
  {
    path: "/",
    component: () => import("@/views/Login/LoginPage.vue"),
  },
  // {
  //   path: "/goal/:id/task",
  //   component: () => import("@/views/TaskDetails/TaskDetailsPage.vue"),
  // },
  // {
  //   path: "/tasks",
  //   component: () => import("@/views/TaskList/TaskListPage.vue"),
  // },
];

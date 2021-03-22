import Vue from "vue";
import VueRouter from "vue-router";
import { routes } from "./routes.js";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

if (process.env.NODE_ENV === "development") {
  router.addRoutes([
    {
      path: "/__test__",
      component: () => import("@/views/Test/TestPage.vue"),
    },
  ]);
}

export default router;

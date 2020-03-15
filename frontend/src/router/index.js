import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Reports from "../views/Reports.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login
  },
  {
    path: "/home",
    name: "Home",
    component: Home
  },
  {
    path: "/reports",
    name: "Reports",
    component: Reports
  },
  {
    path: "/about",
    name: "About",
    component: About.vue
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;

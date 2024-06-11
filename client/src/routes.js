import Dashboard from "views/Dashboard.js";
import UserProfile from "views/UserProfile.js";

import Login from "views/Login";
import Logout from "views/Logout";


const dashboardRoutes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "nc-icon nc-chart-pie-35",
    component: Dashboard,
    layout: "/admin"
  },
  {
    path: "/user",
    name: "Subscription Form",
    icon: "nc-icon nc-circle-09",
    component: UserProfile,
    layout: "/admin"
  },

  {
    path: "/logout",
    name: "log out",
    icon: "nc-icon nc-bell-55",
    component: Logout,
    layout: "/admin"
  }
];

export const authRoutes = [
  {
    path: "/login",
    name: "Login",
    icon: "nc-icon nc-key-25",
    component: Login,
    layout: "/auth"
  }
];

export default dashboardRoutes;

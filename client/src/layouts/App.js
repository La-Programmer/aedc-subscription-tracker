import React from "react";
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
import Admin from "layouts/Admin";
import Login from "views/Login";
import dashboardRoutes, { authRoutes } from "routes.js";

const PrivateRoute = ({ component: Component, ...rest }) => {
  const isAuthenticated = !!localStorage.getItem("authToken"); // Replace with your auth logic

  return (
    <Route
      {...rest}
      render={(props) =>
        isAuthenticated ? (
          <Component {...props} />
        ) : (
          <Redirect to="/auth/login" />
        )
      }
    />
  );
};

const App = () => {
  return (
    <Router>
      <Switch>
        {authRoutes.map((prop, key) => {
          return (
            <Route
              path={prop.layout + prop.path}
              component={prop.component}
              key={key}
            />
          );
        })}
        {dashboardRoutes.map((prop, key) => {
          return (
            <PrivateRoute
              path={prop.layout + prop.path}
              component={prop.component}
              key={key}
            />
          );
        })}
        <Redirect from="/" to="/auth/login" />
      </Switch>
    </Router>
  );
};

export default App;

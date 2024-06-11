import React, { useEffect } from "react";
import { useHistory } from "react-router-dom";

function Logout() {
  const history = useHistory();

  useEffect(() => {
    // Clear authentication token
    localStorage.removeItem("authToken");
    // Redirect to login page
    history.push("/auth/login");
  }, [history]);

  return (
    <div>
      <p>Logging out...</p>
    </div>
  );
}

export default Logout;

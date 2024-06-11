import React, { useState } from "react";
import { useHistory } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const history = useHistory();

  const handleLogin = (e) => {
    e.preventDefault();
    // Your authentication logic here
    // If authentication is successful:
    localStorage.setItem("authToken", "your-auth-token"); // Example, replace with your logic
    history.push("/admin/dashboard");
  };

  return (
    <div className="login-page" style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", height: "100vh", backgroundColor: "#f0f0f0" }}>
      <div style={{ display: "flex", alignItems: "center", marginBottom: "20px", textAlign: "center" }}>
        <img
          className="d-none d-lg-block"
          style={{ width: '100px', height: '26px', marginRight: '10px' }}
          src={require('assets/img/aedc-logo.png')}
          alt="..."
        />
        <p style={{ fontFamily: "OpenSans", fontSize: "15px", fontWeight: "bold", margin: 0, color: "darkblue" }}>Subscription Management System</p>
      </div>
      <div className="login-container" style={{ width: "30%", textAlign: "center", boxShadow: "0 0 10px rgba(0, 0, 255, 0.5)", padding: "20px", borderRadius: "10px", backgroundColor: "#ffffff" }}>
        <h2 style={{color: "darkblue"}}>Login</h2>
        <p style={{fontFamily: "openSans"}}>Please log in to continue</p>
        <form onSubmit={handleLogin} style={{ textAlign: "left" }}>
          <div className="form-group">
            <label style={{ marginBottom: "5px", fontFamily: "OpenSans", fontWeight: "bolder" }}>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="form-control"
             
              style={{ opacity: 0.7, borderRadius: "10px", border: "1px solid #ced4da", padding: "8px" }}
            />
          </div>
          <div className="form-group">
            <label style={{ marginBottom: "5px", fontFamily: "OpenSans", fontWeight: "bolder" }}>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-control"
            
              style={{ opacity: 0.7, borderRadius: "10px", border: "1px solid #ced4da", padding: "8px" }}
            />
          </div>
          <button type="submit" className="btn btn-primary" style={{backgroundColor: "#0a58ca", color: "white"}}>Login</button>
        </form>
      </div>
    </div>
  );
}

export default Login;

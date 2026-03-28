import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { loginUser } from "../services/api";

function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [credentials, setCredentials] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;
    setCredentials((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!credentials.email || !credentials.password) {
      setError("Email and password are required");
      return;
    }

    try {
      const user = await loginUser(credentials);
      login(user);
      navigate("/dashboard");
    } catch (apiError) {
      const message =
        apiError.code === "ERR_NETWORK"
          ? "Cannot connect to backend server. Start JSON Server on port 3000 and try again."
          : apiError.message || "Unable to login";
      setError(message);
    }
  };

  return (
    <main className="page">
      <form className="panel auth" onSubmit={handleSubmit}>
        <h2>Login</h2>
        {error && <p className="error">{error}</p>}
        <input
          name="email"
          placeholder="Email"
          value={credentials.email}
          onChange={handleChange}
        />
        <input
          name="password"
          placeholder="Password"
          type="password"
          value={credentials.password}
          onChange={handleChange}
        />
        <button type="submit">Login</button>
        <p>
          New user? <Link to="/register">Register</Link>
        </p>
      </form>
    </main>
  );
}

export default Login;

import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../services/api";

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!formData.name || !formData.email || !formData.password) {
      setError("All fields are required");
      setSuccess("");
      return;
    }

    try {
      await registerUser(formData);
      setError("");
      setSuccess("Registration successful. You can now login.");
      setTimeout(() => navigate("/login"), 600);
    } catch (apiError) {
      const message =
        apiError.code === "ERR_NETWORK"
          ? "Cannot connect to backend server. Start JSON Server on port 3000 and try again."
          : apiError.message || "Registration failed";
      setError(message);
      setSuccess("");
    }
  };

  return (
    <main className="page">
      <form className="panel auth" onSubmit={handleSubmit}>
        <h2>Create Account</h2>
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
        <input name="name" placeholder="Name" value={formData.name} onChange={handleChange} />
        <input name="email" placeholder="Email" value={formData.email} onChange={handleChange} />
        <input
          name="password"
          placeholder="Password"
          type="password"
          value={formData.password}
          onChange={handleChange}
        />
        <button type="submit">Register</button>
        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </main>
  );
}

export default Register;

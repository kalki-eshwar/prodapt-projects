import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const navigate = useNavigate();
  const { user, role, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <header className="navbar">
      <h2>Secure Product Management</h2>
      <nav>
        <Link to="/dashboard">Dashboard</Link>
        <span className="role-chip">{role || "guest"}</span>
        <span>{user?.name}</span>
        <button type="button" onClick={handleLogout}>
          Logout
        </button>
      </nav>
    </header>
  );
}

export default Navbar;

import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  if (!user) return null;

  return (
    <nav style={{ padding: "10px", background: "#f0f0f0", display: "flex", justifyContent: "space-between" }}>
      <div>
        <Link to="/dashboard" style={{ marginRight: "15px" }}>Dashboard</Link>
      </div>
      <div>
        <span style={{ marginRight: "15px" }}>Welcome, {user.name}</span>
        <button onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  );
};

export default Navbar;

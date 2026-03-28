import React from "react";
import { Link } from "react-router-dom";

function Landing() {
  return (
    <main className="page center">
      <h1>Smart Inventory Management System</h1>
      <p>Track stock, manage products, and keep your retail operations in sync.</p>
      <div className="actions">
        <Link className="button-link" to="/login">
          Login
        </Link>
        <Link className="button-link muted" to="/register">
          Register
        </Link>
      </div>
    </main>
  );
}

export default Landing;

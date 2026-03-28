import React from "react";
import { Link } from "react-router-dom";

function Landing() {
  return (
    <main className="page center">
      <h1>Secure Product Management System</h1>
      <p>JWT-based authentication with role-based access for product operations.</p>
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

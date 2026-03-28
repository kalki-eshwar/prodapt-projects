import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "../App";
import Dashboard from "../pages/Dashboard";
import { fetchProducts } from "../services/api";

const authState = {
  token: "jwt-token-admin",
  role: "admin",
  user: { name: "Admin" },
  isAuthenticated: true,
};

jest.mock("../context/AuthContext", () => ({
  useAuth: () => authState,
}));

jest.mock("../services/api", () => ({
  loginUser: jest.fn(),
  registerUser: jest.fn(),
  fetchProducts: jest.fn(),
  createProduct: jest.fn(),
  updateProduct: jest.fn(),
  deleteProduct: jest.fn(),
}));

describe("RBAC", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("admin can access product form", async () => {
    authState.role = "admin";
    authState.user = { name: "Admin" };
    authState.token = "jwt-token-admin";
    authState.isAuthenticated = true;
    fetchProducts.mockResolvedValue([]);

    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    expect(await screen.findByRole("heading", { name: /add product/i })).toBeInTheDocument();
  });

  test("user cannot access admin features", async () => {
    authState.role = "user";
    authState.user = { name: "User" };
    authState.token = "jwt-token-user";
    authState.isAuthenticated = true;
    fetchProducts.mockResolvedValue([
      { id: 1, title: "Watch", price: 2000, category: "Electronics" },
    ]);

    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    expect(await screen.findByText(/read-only access/i)).toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: /add product/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /edit/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /delete/i })).not.toBeInTheDocument();
  });

  test("unauthorized admin route is blocked", async () => {
    authState.role = "user";
    authState.user = { name: "User" };
    authState.token = "jwt-token-user";
    authState.isAuthenticated = true;
    fetchProducts.mockResolvedValue([]);

    render(
      <MemoryRouter initialEntries={["/admin"]}>
        <App />
      </MemoryRouter>
    );

    expect(await screen.findByText(/role-based product management dashboard/i)).toBeInTheDocument();
  });
});

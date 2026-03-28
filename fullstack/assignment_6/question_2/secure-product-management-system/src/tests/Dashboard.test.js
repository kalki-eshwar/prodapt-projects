import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Dashboard from "../pages/Dashboard";
import { fetchProducts } from "../services/api";

const authState = {
  token: "jwt-token-user",
  role: "user",
  user: { name: "User" },
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

describe("Dashboard", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("products load successfully", async () => {
    fetchProducts.mockResolvedValue([{ id: 1, title: "Smart Watch", price: 3000, category: "Electronics" }]);

    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    expect(await screen.findByText(/smart watch/i)).toBeInTheDocument();
  });

  test("loading state handled", async () => {
    fetchProducts.mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve([]), 100))
    );

    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test("error state handled", async () => {
    fetchProducts.mockRejectedValue(new Error("network"));

    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    expect(await screen.findByText(/failed to fetch products/i)).toBeInTheDocument();
  });
});

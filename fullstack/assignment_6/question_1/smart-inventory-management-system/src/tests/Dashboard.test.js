import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "../App";
import Dashboard from "../pages/Dashboard";
import { fetchProducts } from "../services/api";

const authState = {
  user: null,
  isAuthenticated: false,
};

jest.mock("../context/AuthContext", () => ({
  useAuth: () => authState,
}));

jest.mock("../services/api", () => ({
  fetchProducts: jest.fn(),
  createProduct: jest.fn(),
  updateProduct: jest.fn(),
  deleteProduct: jest.fn(),
}));

describe("Dashboard and protected route", () => {
  afterEach(() => {
    localStorage.clear();
    authState.user = null;
    authState.isAuthenticated = false;
    jest.clearAllMocks();
  });

  test("protected route blocks unauthenticated user", async () => {
    authState.user = null;
    authState.isAuthenticated = false;

    render(
      <MemoryRouter initialEntries={["/dashboard"]}>
        <App />
      </MemoryRouter>
    );

    expect(await screen.findByRole("heading", { name: /login/i })).toBeInTheDocument();
  });

  test("data fetch success", async () => {
    authState.user = { name: "Ravi" };
    authState.isAuthenticated = true;

    fetchProducts.mockResolvedValue([{ id: 1, title: "Headphones", price: 1500, category: "Electronics" }]);

    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    expect(await screen.findByText(/headphones/i)).toBeInTheDocument();
  });

  test("loading state handling", async () => {
    authState.user = { name: "Ravi" };
    authState.isAuthenticated = true;

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

  test("error handling", async () => {
    authState.user = { name: "Ravi" };
    authState.isAuthenticated = true;

    fetchProducts.mockRejectedValue(new Error("network error"));

    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    expect(await screen.findByText(/failed to fetch products/i)).toBeInTheDocument();
  });
});

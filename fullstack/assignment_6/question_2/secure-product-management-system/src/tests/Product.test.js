import React from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Dashboard from "../pages/Dashboard";
import {
  createProduct,
  deleteProduct,
  fetchProducts,
  updateProduct,
} from "../services/api";

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

const renderDashboard = () =>
  render(
    <MemoryRouter>
      <Dashboard />
    </MemoryRouter>
  );

describe("Product management", () => {
  beforeEach(() => {
    authState.role = "admin";
    authState.user = { name: "Admin" };
    authState.token = "jwt-token-admin";
    authState.isAuthenticated = true;
    jest.clearAllMocks();
  });

  test("admin can add product", async () => {
    fetchProducts.mockResolvedValue([]);
    createProduct.mockResolvedValue({
      id: 1,
      title: "Watch",
      price: 2000,
      category: "Electronics",
    });

    renderDashboard();
    await waitFor(() => expect(fetchProducts).toHaveBeenCalled());

    fireEvent.change(screen.getByPlaceholderText("Title"), {
      target: { value: "Watch" },
    });
    fireEvent.change(screen.getByPlaceholderText("Price"), {
      target: { value: "2000" },
    });
    fireEvent.change(screen.getByPlaceholderText("Category"), {
      target: { value: "Electronics" },
    });
    fireEvent.submit(screen.getByLabelText("product-form"));

    await waitFor(() => expect(createProduct).toHaveBeenCalledTimes(1));
  });

  test("admin can update product", async () => {
    fetchProducts.mockResolvedValue([{ id: 1, title: "Watch", price: 2000, category: "Electronics" }]);
    updateProduct.mockResolvedValue({ id: 1, title: "Watch Pro", price: 3000, category: "Electronics" });

    renderDashboard();

    fireEvent.click(await screen.findByRole("button", { name: /edit/i }));
    fireEvent.change(screen.getByPlaceholderText("Title"), {
      target: { value: "Watch Pro" },
    });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => expect(updateProduct).toHaveBeenCalledTimes(1));
  });

  test("admin can delete product", async () => {
    fetchProducts.mockResolvedValue([{ id: 7, title: "Phone", price: 25000, category: "Electronics" }]);
    deleteProduct.mockResolvedValue();

    renderDashboard();

    fireEvent.click(await screen.findByRole("button", { name: /delete/i }));

    await waitFor(() => expect(deleteProduct).toHaveBeenCalledWith(7));
  });

  test("user cannot perform write actions", async () => {
    authState.role = "user";
    authState.user = { name: "User" };
    authState.token = "jwt-token-user";
    authState.isAuthenticated = true;
    fetchProducts.mockResolvedValue([{ id: 9, title: "Headphones", price: 1500, category: "Electronics" }]);

    renderDashboard();

    await screen.findByText(/headphones/i);
    expect(screen.queryByRole("button", { name: /add product/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /edit/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /delete/i })).not.toBeInTheDocument();
  });
});

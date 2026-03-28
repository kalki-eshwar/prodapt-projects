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

jest.mock("../context/AuthContext", () => ({
  useAuth: () => ({ user: { name: "Ravi" } }),
}));

jest.mock("../services/api", () => ({
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

describe("Product workflows", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("fetch product list", async () => {
    fetchProducts.mockResolvedValue([
      { id: 1, title: "Headphones", price: 1500, category: "Electronics" },
    ]);

    renderDashboard();

    expect(await screen.findByText(/headphones/i)).toBeInTheDocument();
    expect(fetchProducts).toHaveBeenCalled();
  });

  test("add product", async () => {
    fetchProducts.mockResolvedValue([]);
    createProduct.mockResolvedValue({ id: 2, title: "Phone", price: 20000, category: "Electronics" });

    renderDashboard();

    await waitFor(() => expect(fetchProducts).toHaveBeenCalled());

    fireEvent.change(screen.getByPlaceholderText("Title"), {
      target: { value: "Phone" },
    });
    fireEvent.change(screen.getByPlaceholderText("Price"), {
      target: { value: "20000" },
    });
    fireEvent.change(screen.getByPlaceholderText("Category"), {
      target: { value: "Electronics" },
    });
    fireEvent.submit(screen.getByLabelText("product-form"));

    await waitFor(() => expect(createProduct).toHaveBeenCalledTimes(1));
  });

  test("update product", async () => {
    fetchProducts.mockResolvedValue([{ id: 1, title: "Phone", price: 20000, category: "Electronics" }]);
    updateProduct.mockResolvedValue({ id: 1, title: "Phone X", price: 25000, category: "Electronics" });

    renderDashboard();

    fireEvent.click(await screen.findByRole("button", { name: /edit/i }));
    fireEvent.change(screen.getByPlaceholderText("Title"), {
      target: { value: "Phone X" },
    });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => expect(updateProduct).toHaveBeenCalledTimes(1));
  });

  test("delete product", async () => {
    fetchProducts.mockResolvedValue([{ id: 3, title: "Laptop", price: 50000, category: "Electronics" }]);
    deleteProduct.mockResolvedValue();

    renderDashboard();

    fireEvent.click(await screen.findByRole("button", { name: /delete/i }));

    await waitFor(() => expect(deleteProduct).toHaveBeenCalledWith(3));
  });
});

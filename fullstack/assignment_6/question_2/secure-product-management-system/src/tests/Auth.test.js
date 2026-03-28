import React from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Login from "../pages/Login";
import { loginUser } from "../services/api";

const mockLogin = jest.fn();

jest.mock("../context/AuthContext", () => ({
  useAuth: () => ({ login: mockLogin }),
}));

jest.mock("../services/api", () => ({
  loginUser: jest.fn(),
  fetchProducts: jest.fn(),
  createProduct: jest.fn(),
  updateProduct: jest.fn(),
  deleteProduct: jest.fn(),
}));

describe("Auth flows", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("valid login returns token payload", async () => {
    loginUser.mockResolvedValue({
      token: "jwt-token-admin",
      role: "admin",
      user: { id: 1, name: "Admin" },
    });

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Email"), {
      target: { value: "admin@mail.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Password"), {
      target: { value: "1234" },
    });
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => expect(mockLogin).toHaveBeenCalledTimes(1));
  });

  test("invalid login shows error", async () => {
    loginUser.mockRejectedValue(new Error("Invalid email or password"));

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Email"), {
      target: { value: "bad@mail.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Password"), {
      target: { value: "bad" },
    });
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    expect(await screen.findByText(/invalid email or password/i)).toBeInTheDocument();
  });

  test("token payload is passed to context login", async () => {
    const payload = {
      token: "jwt-token-user",
      role: "user",
      user: { id: 2, name: "User" },
    };
    loginUser.mockResolvedValue(payload);

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Email"), {
      target: { value: "user@mail.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Password"), {
      target: { value: "1234" },
    });
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => expect(mockLogin).toHaveBeenCalledWith(payload));
  });
});

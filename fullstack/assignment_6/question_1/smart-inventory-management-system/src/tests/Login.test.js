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
}));

describe("Login page", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("valid login shows success path", async () => {
    loginUser.mockResolvedValue({ id: 1, name: "Ravi", email: "ravi@mail.com" });

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Email"), {
      target: { value: "ravi@mail.com" },
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
      target: { value: "wrong@mail.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Password"), {
      target: { value: "wrong" },
    });
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    expect(await screen.findByText(/invalid email or password/i)).toBeInTheDocument();
  });

  test("empty fields show validation error", async () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    expect(await screen.findByText(/email and password are required/i)).toBeInTheDocument();
    expect(loginUser).not.toHaveBeenCalled();
  });
});

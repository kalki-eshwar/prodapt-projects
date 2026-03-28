import React from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Register from "../pages/Register";
import { registerUser } from "../services/api";

jest.mock("../services/api", () => ({
  registerUser: jest.fn(),
}));

describe("Register page", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("successful registration", async () => {
    registerUser.mockResolvedValue({ id: 1, name: "Ravi" });

    render(
      <MemoryRouter>
        <Register />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Name"), {
      target: { value: "Ravi" },
    });
    fireEvent.change(screen.getByPlaceholderText("Email"), {
      target: { value: "ravi@mail.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Password"), {
      target: { value: "1234" },
    });

    fireEvent.click(screen.getByRole("button", { name: /register/i }));

    expect(await screen.findByText(/registration successful/i)).toBeInTheDocument();
  });

  test("duplicate email shows error", async () => {
    registerUser.mockRejectedValue(new Error("Email already registered"));

    render(
      <MemoryRouter>
        <Register />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Name"), {
      target: { value: "Ravi" },
    });
    fireEvent.change(screen.getByPlaceholderText("Email"), {
      target: { value: "ravi@mail.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Password"), {
      target: { value: "1234" },
    });

    fireEvent.click(screen.getByRole("button", { name: /register/i }));

    expect(await screen.findByText(/email already registered/i)).toBeInTheDocument();
  });

  test("required field validation", async () => {
    render(
      <MemoryRouter>
        <Register />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /register/i }));

    await waitFor(() => {
      expect(screen.getByText(/all fields are required/i)).toBeInTheDocument();
    });
    expect(registerUser).not.toHaveBeenCalled();
  });
});

import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:3000",
});

export const registerUser = async (payload) => {
  const duplicate = await api.get(`/users?email=${encodeURIComponent(payload.email)}`);
  if (duplicate.data.length > 0) {
    throw new Error("Email already registered");
  }

  const response = await api.post("/users", payload);
  return response.data;
};

export const loginUser = async ({ email, password }) => {
  const response = await api.get(`/users?email=${encodeURIComponent(email)}`);
  const user = response.data.find((item) => item.password === password);

  if (!user) {
    throw new Error("Invalid email or password");
  }

  return user;
};

export const fetchProducts = async () => {
  const response = await api.get("/products");
  return response.data;
};

export const createProduct = async (payload) => {
  const response = await api.post("/products", payload);
  return response.data;
};

export const updateProduct = async (id, payload) => {
  const response = await api.put(`/products/${id}`, payload);
  return response.data;
};

export const deleteProduct = async (id) => {
  await api.delete(`/products/${id}`);
};

export default api;

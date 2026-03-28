import React, { useEffect, useMemo, useState } from "react";
import Navbar from "../components/Navbar";
import ProductForm from "../components/ProductForm";
import ProductList from "../components/ProductList";
import { useAuth } from "../context/AuthContext";
import { createProduct, deleteProduct, fetchProducts, updateProduct } from "../services/api";

function Dashboard() {
  const { user } = useAuth();
  const [products, setProducts] = useState([]);
  const [editingProduct, setEditingProduct] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState({ type: "", message: "" });

  const fetchAllProducts = async () => {
    setLoading(true);
    try {
      const data = await fetchProducts();
      setProducts(data);
      setStatus({ type: "", message: "" });
    } catch (error) {
      const message =
        error.code === "ERR_NETWORK"
          ? "Cannot connect to backend server. Start JSON Server on port 3000 and refresh."
          : "Failed to fetch products";
      setStatus({ type: "error", message });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllProducts();
  }, []);

  const handleSubmitProduct = async (payload) => {
    setLoading(true);
    try {
      if (editingProduct) {
        await updateProduct(editingProduct.id, payload);
        setStatus({ type: "success", message: "Product updated successfully" });
      } else {
        await createProduct(payload);
        setStatus({ type: "success", message: "Product added successfully" });
      }

      setEditingProduct(null);
      await fetchAllProducts();
    } catch (error) {
      const message =
        error.code === "ERR_NETWORK"
          ? "Cannot connect to backend server. Start JSON Server on port 3000 and try again."
          : "Failed to save product";
      setStatus({ type: "error", message });
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    setLoading(true);
    try {
      await deleteProduct(id);
      setStatus({ type: "success", message: "Product deleted successfully" });
      await fetchAllProducts();
    } catch (error) {
      const message =
        error.code === "ERR_NETWORK"
          ? "Cannot connect to backend server. Start JSON Server on port 3000 and try again."
          : "Failed to delete product";
      setStatus({ type: "error", message });
      setLoading(false);
    }
  };

  const greeting = useMemo(() => `Welcome, ${user?.name || "User"}!`, [user]);

  return (
    <>
      <Navbar />
      <main className="page">
        <h2>{greeting}</h2>
        <p>Manage your inventory from one place.</p>

        {status.message && (
          <p className={status.type === "error" ? "error" : "success"}>{status.message}</p>
        )}

        <ProductForm
          onSubmit={handleSubmitProduct}
          editingProduct={editingProduct}
          onCancelEdit={() => setEditingProduct(null)}
          loading={loading}
        />

        {loading && <p>Loading...</p>}

        <ProductList products={products} onEdit={setEditingProduct} onDelete={handleDelete} />
      </main>
    </>
  );
}

export default Dashboard;

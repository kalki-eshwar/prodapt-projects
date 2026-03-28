import React, { useState, useEffect } from "react";
import api from "../services/api";
import ProductForm from "../components/ProductForm";
import ProductList from "../components/ProductList";

const Dashboard = () => {
  const [products, setProducts] = useState([]);
  const [editingProduct, setEditingProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await api.get("/products");
      setProducts(response.data);
      setLoading(false);
    } catch (err) {
      setError("Error fetching products");
      setLoading(false);
    }
  };

  const handleProductAdded = (newProduct) => {
    setProducts([...products, newProduct]);
  };

  const handleProductUpdated = (updatedProduct) => {
    if (updatedProduct) {
      setProducts(
        products.map((p) =>
          String(p.id) === String(updatedProduct.id) ? updatedProduct : p
        )
      );
    }
    setEditingProduct(null);
  };

  const handleProductDeleted = (id) => {
    setProducts(products.filter(p => p.id !== id));
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div style={{ maxWidth: "800px", margin: "20px auto" }}>
      <h2>Dashboard</h2>
      <ProductForm 
        onProductAdded={handleProductAdded} 
        editingProduct={editingProduct} 
        onProductUpdated={handleProductUpdated} 
      />
      <ProductList 
        products={products} 
        onEdit={setEditingProduct} 
        onDelete={handleProductDeleted} 
      />
    </div>
  );
};

export default Dashboard;

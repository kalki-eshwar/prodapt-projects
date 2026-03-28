import React, { useState, useEffect } from "react";
import api from "../services/api";

const ProductForm = ({ onProductAdded, editingProduct, onProductUpdated }) => {
  const [formData, setFormData] = useState({ title: "", price: "", category: "" });

  useEffect(() => {
    if (editingProduct) {
      setFormData({
        title: editingProduct.title || "",
        price: editingProduct.price || "",
        category: editingProduct.category || "",
      });
    } else {
      setFormData({ title: "", price: "", category: "" });
    }
  }, [editingProduct]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editingProduct) {
      try {
        const response = await api.put(`/products/${editingProduct.id}`, {
          ...formData,
          id: editingProduct.id,
        });
        onProductUpdated(response.data);
      } catch (err) {
        console.error("Failed to update product");
      }
    } else {
      try {
        const response = await api.post("/products", formData);
        onProductAdded(response.data);
      } catch (err) {
        console.error("Failed to add product");
      }
    }
    setFormData({ title: "", price: "", category: "" });
  };

  return (
    <div style={{ padding: "20px", border: "1px solid #ccc", marginBottom: "20px" }}>
      <h3>{editingProduct ? "Update Product" : "Add Product"}</h3>
      <form onSubmit={handleSubmit} style={{ display: "flex", gap: "10px", alignItems: "center" }}>
        <input 
          type="text" 
          name="title" 
          placeholder="Title" 
          value={formData.title} 
          onChange={handleChange} 
          required 
        />
        <input 
          type="number" 
          name="price" 
          placeholder="Price" 
          value={formData.price} 
          onChange={handleChange} 
          required 
        />
        <input 
          type="text" 
          name="category" 
          placeholder="Category" 
          value={formData.category} 
          onChange={handleChange} 
          required 
        />
        <button type="submit">{editingProduct ? "Update" : "Add"}</button>
        {editingProduct && (
          <button type="button" onClick={() => onProductUpdated(null)}>Cancel</button>
        )}
      </form>
    </div>
  );
};

export default ProductForm;

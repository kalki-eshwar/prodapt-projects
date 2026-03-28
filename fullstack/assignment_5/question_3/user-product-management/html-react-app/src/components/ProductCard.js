import React from "react";
import api from "../services/api";

const ProductCard = ({ product, index, onEdit, onDelete }) => {
  const handleDelete = async () => {
    try {
      await api.delete(`/products/${product.id}`);
      onDelete(product.id);
    } catch (err) {
      console.error("Failed to delete product");
    }
  };

  return (
    <div style={{ display: "flex", justifyContent: "space-between", padding: "10px", borderBottom: "1px solid #eee" }}>
      <div>
        {index + 1}. {product.title} - ₹{product.price} {product.category && `- ${product.category}`}
      </div>
      <div>
        <button onClick={() => onEdit(product)} style={{ marginRight: "10px" }}>Edit</button>
        <button onClick={handleDelete}>Delete</button>
      </div>
    </div>
  );
};

export default ProductCard;

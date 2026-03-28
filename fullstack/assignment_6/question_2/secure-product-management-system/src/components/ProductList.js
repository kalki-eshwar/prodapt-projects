import React from "react";
import ProductCard from "./ProductCard";

function ProductList({ products, onEdit, onDelete }) {
  if (products.length === 0) {
    return <p className="empty">No products available.</p>;
  }

  return (
    <section className="product-grid" aria-label="product-list">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} onEdit={onEdit} onDelete={onDelete} />
      ))}
    </section>
  );
}

export default ProductList;

import React from "react";

function ProductCard({ product, onEdit, onDelete }) {
  return (
    <article className="product-card" data-testid={`product-${product.id}`}>
      <h4>{product.title}</h4>
      <p>Price: Rs. {product.price}</p>
      <p>Category: {product.category}</p>
      <div className="actions">
        <button type="button" onClick={() => onEdit(product)}>
          Edit
        </button>
        <button type="button" className="danger" onClick={() => onDelete(product.id)}>
          Delete
        </button>
      </div>
    </article>
  );
}

export default ProductCard;

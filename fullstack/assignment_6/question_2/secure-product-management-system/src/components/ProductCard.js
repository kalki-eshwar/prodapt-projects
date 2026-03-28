import React from "react";
import RoleBasedView from "./RoleBasedView";

function ProductCard({ product, onEdit, onDelete }) {
  return (
    <article className="product-card" data-testid={`product-${product.id}`}>
      <h4>{product.title}</h4>
      <p>Price: Rs. {product.price}</p>
      <p>Category: {product.category}</p>

      <RoleBasedView allowedRoles={["admin"]}>
        <div className="actions">
          <button type="button" onClick={() => onEdit(product)}>
            Edit
          </button>
          <button type="button" className="danger" onClick={() => onDelete(product.id)}>
            Delete
          </button>
        </div>
      </RoleBasedView>
    </article>
  );
}

export default ProductCard;

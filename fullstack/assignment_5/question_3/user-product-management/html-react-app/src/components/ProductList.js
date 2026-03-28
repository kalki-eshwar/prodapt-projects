import React from "react";
import ProductCard from "./ProductCard";

const ProductList = ({ products, onEdit, onDelete }) => {
  return (
    <div>
      <h3>Products:</h3>
      {products.length === 0 ? (
        <p>No products available.</p>
      ) : (
        products.map((product, index) => (
          <ProductCard 
            key={product.id || `${product.title}-${index}`} 
            index={index} 
            product={product} 
            onEdit={onEdit} 
            onDelete={onDelete} 
          />
        ))
      )}
    </div>
  );
};

export default ProductList;

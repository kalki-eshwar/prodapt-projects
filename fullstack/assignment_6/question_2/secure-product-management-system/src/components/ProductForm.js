import React, { useEffect, useState } from "react";

const initialState = {
  title: "",
  price: "",
  category: "",
};

function ProductForm({ editingProduct, onSubmit, onCancelEdit, loading }) {
  const [formData, setFormData] = useState(initialState);

  useEffect(() => {
    if (editingProduct) {
      setFormData({
        title: editingProduct.title,
        price: String(editingProduct.price),
        category: editingProduct.category,
      });
      return;
    }

    setFormData(initialState);
  }, [editingProduct]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!formData.title || !formData.price || !formData.category) {
      return;
    }

    onSubmit({
      title: formData.title.trim(),
      price: Number(formData.price),
      category: formData.category.trim(),
    });

    if (!editingProduct) {
      setFormData(initialState);
    }
  };

  return (
    <form className="panel" onSubmit={handleSubmit} aria-label="product-form">
      <h3>{editingProduct ? "Update Product" : "Add Product"}</h3>
      <div className="field-grid">
        <input
          name="title"
          placeholder="Title"
          value={formData.title}
          onChange={handleChange}
          required
        />
        <input
          name="price"
          placeholder="Price"
          type="number"
          min="0"
          value={formData.price}
          onChange={handleChange}
          required
        />
        <input
          name="category"
          placeholder="Category"
          value={formData.category}
          onChange={handleChange}
          required
        />
      </div>
      <div className="actions">
        <button type="submit" disabled={loading}>
          {editingProduct ? "Save Changes" : "Add Product"}
        </button>
        {editingProduct && (
          <button type="button" className="muted" onClick={onCancelEdit}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

export default ProductForm;

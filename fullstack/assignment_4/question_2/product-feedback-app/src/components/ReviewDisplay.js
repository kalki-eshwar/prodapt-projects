import React from 'react';

const ReviewDisplay = ({ data, onReset }) => {
  const getReviewMessage = (rating) => {
    switch (Number(rating)) {
      case 1: return 'Poor experience';
      case 2: return 'Needs improvement';
      case 3: return 'Average product 🙂';
      case 4: return 'Good product';
      case 5: return 'Excellent product 🎉';
      default: return '';
    }
  };

  return (
    <div className="review-container">
      <h2>Thank You, {data.name}!</h2>
      <div className="review-details">
        <p><strong>Product:</strong> {data.productName}</p>
        <p><strong>Rating:</strong> {data.rating}</p>
        <p><strong>Review:</strong> {getReviewMessage(data.rating)}</p>
      </div>
      <button onClick={onReset} className="reset-btn">Submit Another Feedback</button>
    </div>
  );
};

export default ReviewDisplay;

import React, { useState } from 'react';
import './App.css';
import FeedbackForm from './components/FeedbackForm';
import ReviewDisplay from './components/ReviewDisplay';

function App() {
  const [feedbackData, setFeedbackData] = useState(null);

  const handleFeedbackSubmit = (data) => {
    setFeedbackData(data);
  };

  const handleReset = () => {
    setFeedbackData(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Product Feedback System</h1>
      </header>
      <main>
        {feedbackData ? (
          <ReviewDisplay data={feedbackData} onReset={handleReset} />
        ) : (
          <FeedbackForm onSubmit={handleFeedbackSubmit} />
        )}
      </main>
    </div>
  );
}

export default App;

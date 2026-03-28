import React from 'react';
import Header from './components/Header';
import Home from './pages/Home';
import { StudentProvider } from './context/StudentContext';

function App() {
  return (
    <StudentProvider>
      <div className="App">
        <Header />
        <Home />
      </div>
    </StudentProvider>
  );
}

export default App;

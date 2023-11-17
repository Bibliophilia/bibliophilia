import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './Style/App.css';
import HomePage from './component/HomePage';
import CategoryWindow from './component/CategoryWindow';
import UploadBooks from './component/UploadBooks';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/category" element={<CategoryWindow />} />
          <Route path="/upload-books" element={<UploadBooks />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

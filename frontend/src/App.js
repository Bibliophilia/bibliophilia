import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './Style/App.css';
import HomePage from './component/Page-Component/HomePage';
import CategoryWindow from './component/Page-Component/CategoryWindow';
import SearchResultsPage from './component/Page-Component/SearchResultsPage';
import UploadBooks from "./component/Component/UploadBooks";
import UserProfile from "./component/User-Component/UserProfile";
import BookInfoPage from "./component/Page-Component/BookInfoPage";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/profile" element={<UserProfile />} />   // testing if user profile is working or not
          <Route path="/category" element={<CategoryWindow />} />
          <Route path="/upload-books" element={<UploadBooks />} />
          <Route path="/search-results" element={<SearchResultsPage />} />
          <Route path="/books/:idx" element={<BookInfoPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

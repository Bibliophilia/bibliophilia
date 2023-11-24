import React, { useState } from 'react';
import './ComponentStyles/CategoryWindow.css';

const CategoryWindow = ({ onClose, onSearch }) => {
  const [authors, setAuthors] = useState(['Author1', 'Author2', 'Author3']);
  const [genres, setGenres] = useState([
    'Fiction',
    'Non-Fiction',
    'Mystery',
    'Science Fiction',
    'Fantasy',
  ]);
  const [publicationYears, setPublicationYears] = useState(['2020', '2021', '2022']);

  const [filters, setFilters] = useState({
    author: [],
    genre: [],
    publicationYear: [],
  });

  const handleCheckboxChange = (category, value) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      [category]: prevFilters[category].includes(value)
        ? prevFilters[category].filter((item) => item !== value)
        : [...prevFilters[category], value],
    }));
  };

  return (
    <div className="category-window">
      <h2>Filter Categories</h2>

      <div className="category-section">
        <h3>Authors</h3>
        <div className="checkbox-container">
          {authors.map((author, index) => (
            <label key={index} className="checkbox-label">
              <input
                type="checkbox"
                checked={filters.author.includes(author)}
                onChange={() => handleCheckboxChange('author', author)}
              />
              {author}
            </label>
          ))}
        </div>
      </div>

      <div className="category-section">
        <h3>Genres</h3>
        <div className="checkbox-container">
          {genres.map((genre, index) => (
            <label key={index} className="checkbox-label">
              <input
                type="checkbox"
                checked={filters.genre.includes(genre)}
                onChange={() => handleCheckboxChange('genre', genre)}
              />
              {genre}
            </label>
          ))}
        </div>
      </div>

      <div className="category-section">
        <h3>Publication Years</h3>
        <div className="checkbox-container">
          {publicationYears.map((year, index) => (
            <label key={index} className="checkbox-label">
              <input
                type="checkbox"
                checked={filters.publicationYear.includes(year)}
                onChange={() => handleCheckboxChange('publicationYear', year)}
              />
              {year}
            </label>
          ))}
        </div>
      </div>

      <div className="button-container">
        <button className="search-filter-button" onClick={() => onSearch(filters)}>
          Search Books
        </button>
        <button className="close-button" onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
};

export default CategoryWindow;

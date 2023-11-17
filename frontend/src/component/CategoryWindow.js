import React, { useState } from 'react';

const CategoryWindow = ({ onClose }) => {
  const [categories, setCategories] = useState([
    'Fiction',
    'Non-Fiction',
    'Mystery',
    'Science Fiction',
    'Fantasy',
  
  ]);

  const [filters, setFilters] = useState({
    author: false,
    genre: false,
    publicationYear: false,
  });

  const handleCheckboxChange = (filter) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      [filter]: !prevFilters[filter],
    }));
  };

  return (
    <div>
      <div>
        <h2>Categories</h2>
        <ul>
          {categories.map((category, index) => (
            <li key={index}>{category}</li>
          ))}
        </ul>
      </div>

      <div>
        <h3>Filter Options</h3>
        {Object.entries(filters).map(([filter, isChecked]) => (
          <label key={filter}>
            <input
              type="checkbox"
              checked={isChecked}
              onChange={() => handleCheckboxChange(filter)}
            />
            {filter.charAt(0).toUpperCase() + filter.slice(1)}
          </label>
        ))}
      </div>

      <div>
        {/* Close Button */}
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default CategoryWindow;

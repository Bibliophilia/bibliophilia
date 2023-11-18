import React, { useState } from 'react';

const SearchBar = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleInputChange = (e) => {
    setSearchTerm(e.target.value);
    // Add any additional search functionality here (to do )
  };

  const handleSearch = () => {
    // Implement search functionality using the 'searchTerm' state , ( to do )
    console.log(`Searching for: ${searchTerm}`);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search for books, Articles, Document "
        value={searchTerm}
        onChange={handleInputChange}
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

export default SearchBar;

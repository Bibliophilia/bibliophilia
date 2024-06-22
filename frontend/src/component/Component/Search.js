import React, {useEffect, useState} from 'react';
import searchIcon from '../ComponentStyles/Img/Search_Icon.png';
import {SearchApi} from "../Component-APIs/SearchApi";

const Search = ({ onSearch, onInput}) => {
  const searchApi = new SearchApi();
  const [facetTypes, setFacetTypes] = useState([])
  const [searchTerm, setSearchTerm] = useState('');
  const [currentFacet, setCurrentFacet] = useState('');
  const [hints, setHints] = useState([]);

  useEffect(() => {

    searchApi.getFacets().then(data => setFacetTypes(data)).catch(err => console.log(err));
  }, []);
  function updateFacet(event, query) {
    const cursorPosition = event.target.selectionStart;
    const facetPattern = /(\w+):"([^"]*)"/g;
    let match;
    let foundFacet = null;
    while ((match = facetPattern.exec(query)) !== null) {
      const start = match.index;
      const end = facetPattern.lastIndex;
      if (cursorPosition > start && cursorPosition < end && facetTypes.includes(match[1])) {
        foundFacet = {key: match[1], value: match[2], start, end};
        break;
      }
    }
    setCurrentFacet(foundFacet);
  }

  const handleSearchChange = (event) => {
    const query = event.target.value;
    setSearchTerm(query);
    onInput(event);
    updateFacet(event, query);
    if (currentFacet) {
      setHints([]);
      searchApi.getHints(currentFacet.key, currentFacet.value)
          .then(data => setHints(data))
          .catch(error => {
            console.log(error);
            setHints([]);
          });
    }
    else {
      setHints([]);
    }
  };

  const handleSearch = async () => {
    onSearch(searchTerm)
  };
  const handleSuggestionClick = (suggestion) => {
    if (currentFacet) {
      suggestion = `${searchTerm.slice(0, currentFacet.start)}${currentFacet.key}:"${suggestion}"${searchTerm.slice(currentFacet.end)}`;
      console.log(`${suggestion} applied`);
    }
    setSearchTerm(suggestion);
    setCurrentFacet(null);
    setHints([]);
  };

  return (
    <div className='Search'>
      <div className='SearchBar'>
        <div className="SearchIconContainer" onClick={handleSearch}>
          <img
            className="SearchIcon"
            src={searchIcon}
            alt="Search"
          />
        </div>
        <input
          className=''
          type="text"
          placeholder="Search for books, articles, documents..."
          value={searchTerm}
          onChange={handleSearchChange}
        />
        {hints.length > 0 && (
          <ul className='HintsList'>
            {hints.map((hint, index) => (
              <li key={index} onClick={() => handleSuggestionClick(hint)}>
                {hint}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Search;
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../ComponentStyles/SearchResult.css';
import { SearchApi } from "component/Component-APIs/SearchApi";

const SearchResultsPage = () => {
    const location = useLocation();
    const navigate = useNavigate();

    const searchParams = new URLSearchParams(location.search);
    const searchTerm = searchParams.get('q');

    const [searchResults, setSearchResults] = useState([]);
    const [error, setError] = useState(null);
    const api = new SearchApi();

    useEffect(() => {
        api.search(searchTerm,1)
            .then(data => {
               console.log('API response:', data);
               if (Array.isArray(data) && data.length > 0 && data[0].image_url) {
               setSearchResults(data);
               } else {
                   setError('Oops! No search results found, Try again!');
               }
            })
            .catch(error => {
                console.log('Error fetching search results:', error);
                setError('Error fetching search results. Please try again later.');
            });
    }, [searchTerm]);

    const handleResultItemClick = (idx) => {
        // Navigate to the BookInfoPage for the selected book
        navigate(`/books/${idx}`);
    };

    const navigateToHome = () => {
        navigate('/');
    };

    return (
        <div className="SearchResult-page">
            <div className="SP-header" onClick={navigateToHome}>
                <h1 className="SP-page-title">Bibliophilia</h1>
            </div>

            <h2>Search Results for: {searchTerm}</h2>
            {error ? (
                <p>{error}</p>
            ) : (
                <div className="search-results-container">
                    {searchResults.map((result) => (
                        <div
                            key={result.idx}
                            className="search-result-item"
                            onClick={() => handleResultItemClick(result.idx)}
                        >
                            <img
                                className="search-result-image"
                                src={result.image_url}
                                alt={result.title}
                                onError={(e) => {
                                    console.error(`Error loading image for ${result.title}: ${e}`);
                                    e.target.onerror = null; // Remove the event listener to prevent an infinite loop
                                }}
                            />
                            <div className="search-result-info">
                                <h3 className="search-result-title">{result.title}</h3>
                                <p className="search-result-author">{result.author}</p>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SearchResultsPage;

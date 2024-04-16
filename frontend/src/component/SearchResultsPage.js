import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ComponentStyles/SearchResult.css';

const SearchResultsPage = () => {
    const location = useLocation();
    const navigate = useNavigate();

    const searchParams = new URLSearchParams(location.search);
    const searchTerm = searchParams.get('q');

    const [searchResults, setSearchResults] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Fetch data from your API using searchTerm
        const fetchData = async () => {
            try {
                const response = await fetch(`http://localhost:8000/books/search/?q=${searchTerm}&page=1`);
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                console.log('API response:', data);

                if (Array.isArray(data) && data.length > 0 && data[0].image_url) {
                    setSearchResults(data);
                } else {
                    setError('Oops! No search results found, Try again!', data);
                }
            } catch (error) {
                console.error('Error fetching search results:', error);
                setError('Error fetching search results. Please try again later.');
            }
        };

        fetchData();
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
            <div className="SP-bar-for-title" onClick={navigateToHome}>
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
                                    console.error(`Error loading image for ${result.title}:`, e);
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

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CategoryWindow from './CategoryWindow';
import './ComponentStyles/HomePage.css';
import searchIcon from './ComponentStyles/Img/Search_Icon.png';
import SearchResultsPage from "./SearchResultsPage";

const HomePage = () => {
    const navigate = useNavigate();
    const [isCategoryWindowOpen, setCategoryWindowOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');

    const handleCategoryButtonClick = () => {
        setCategoryWindowOpen(true);
    };

    const handleCloseCategoryModal = () => {
        setCategoryWindowOpen(false);
    };

    const handleUploadButtonClick = () => {
        navigate('/upload-books');
    };

    const handleSearchClick = () => {
        // Navigate to the search results page with the search term as a query parameter
        navigate(`/search-results?q=${searchTerm}&page=1`);
    };

    const handleInputChange = (e) => {
        setSearchTerm(e.target.value);
    };

    return (
        <div className='HomePage'>
            <div className='Upper-Part'>
                <div className='TitleSection'>
                    <h1 className='Title'>Bibliophilia</h1>
                    <p className='subtitle'>A free online platform for bookworms </p>
                </div>
            </div>

            {/* Search Bar Component */}
            <div className='Search'>
                <div className='SearchBar'>
                    <div className="SearchIconContainer" onClick={handleSearchClick}>
                        <img
                            className="SearchIcon"
                            src={searchIcon}
                            alt="Search"
                        />
                    </div>
                    <input className='' type="text" placeholder="Search for books, articles, documents..." value={searchTerm} onChange={handleInputChange} />
                </div>
            </div>

            <div className='CategorySection'>
                {/* Category Button */}
                <p className='category-para'>Get your books by</p>
                <button className="CategoryButton" onClick={handleCategoryButtonClick} >Category</button>

                {/* Category Modal */}
                {isCategoryWindowOpen && <CategoryWindow onClose={handleCloseCategoryModal} />}
            </div>

            <div className='Upload-area'>
                <h2 className='upload-title'>Do you want to be a contributor?</h2>
                <p className='upload-subtitle'>Share your books with the world </p>

                {/* Upload Button */}
                <button className="Upload-button" onClick={handleUploadButtonClick}>Tap to Upload Book</button>
            </div>
        </div>
    );
};

export default HomePage;

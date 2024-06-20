import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import CategoryWindow from './CategoryWindow';
import '../ComponentStyles/HomePage.css';
import Search from "../Search";
import LoginPopup from "../User-Component/UserAuth";

const HomePage = () => {
    const navigate = useNavigate();
    const [isCategoryWindowOpen, setCategoryWindowOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [isLoginPopupOpen, setLoginPopupOpen] = useState(false);
    const loginPopupRef = useRef(null);

    useEffect(() => {
        const handleOutsideClick = (event) => {
            if (loginPopupRef.current && !loginPopupRef.current.contains(event.target)) {
                // Click occurred outside the popup, close the popup
                setLoginPopupOpen(false);
            }
        };

        document.addEventListener('mousedown', handleOutsideClick);

        return () => {
            document.removeEventListener('mousedown', handleOutsideClick);
        };
    }, []);

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
        navigate(`/search-results?q=${searchTerm}&page=1`);
    };

    const handleInputChange = (e) => {
        setSearchTerm(e.target.value);
    };

    const handleLoginButtonClick = () => {
        setLoginPopupOpen(true);
    };

    return (
        <div className='HomePage'>
            <div className='Upper-Part'>
                <div className='TitleSection'>
                    <h1 className='Title'>Bibliophilia</h1>
                    <p className='subtitle'>A free online platform for bookworms </p>
                    <button className='UserAuth-login' onClick={handleLoginButtonClick}>LOGIN</button>
                    {isLoginPopupOpen && (
                        <div className="PopupContainer" ref={loginPopupRef}>
                            <LoginPopup />
                        </div>
                    )}
                    {isLoginPopupOpen && (
                        <div className="PopupOverlay" />
                    )}

                </div>
            </div>

            {/* Search Bar Component */}
            <Search onSearch={handleSearchClick} />

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

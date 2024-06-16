import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useLocation, useNavigate } from 'react-router-dom';
import '../ComponentStyles/BookInfoPage.css'

const BookInfoPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { idx } = useParams();
    const [bookInfo, setBookInfo] = useState(null);
    const [selectedFormat, setSelectedFormat] = useState('');
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchBookInfo = async () => {
            try {
                const response = await fetch(`http://localhost:8000/books/${idx}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                setBookInfo(data);
            } catch (error) {
                console.error('Error fetching book details:', error);
                setError('Error fetching book details. Please try again later.');
            }
        };

        fetchBookInfo();
    }, [idx]);

    const handleReadOnline = () => {
        if (bookInfo && bookInfo.file_url) {
            window.open(bookInfo.file_url, '_blank');
        } else {
            console.error('Book file URL is missing or invalid.');
        }
    };

    const handleDownload = () => {
        if (selectedFormat && bookInfo && bookInfo.formats.includes(selectedFormat)) {
            // Trigger the download using the selected format
            window.location.href = `http://localhost:8000/books/download/?idx=${idx}&book_format=${selectedFormat}`;
        } else {
            setError('Selected format is not available. Please choose a different format.');
        }
    };

    const handleFormatSelect = (e) => {
        setSelectedFormat(e.target.value);
    };

    const navigateToHome = () => {
        navigate('/');
    };

    return (
        <div className="Book-info-page-container">
            <div className="SP-bar-for-title" onClick={navigateToHome}>
                <h1 className="SP-page-title">Bibliophilia</h1>
            </div>
            {error ? (
                <p>{error}</p>
            ) : bookInfo ? (
                <div>
                    <div><h2 className="book-title-bookinfo">{bookInfo.title}</h2></div>

                    <div>
                    <p className="book-author-bookinfo">{bookInfo.author}</p>
                    </div>
                    <div>
                    <p className="book-description-bookinfo">{bookInfo.description}</p>
                    </div>
                    <div>
                    <img className="book-cover-img" src={bookInfo.image_url} alt={bookInfo.title}/>
                    </div>

                    <button className="read-now-button" onClick={handleReadOnline}>Read Now</button>

                    <div>
                        <button className="download-button" onClick={handleDownload}>Download</button>
                        <select className="dropdown-box-bookinfo" onChange={handleFormatSelect} value={selectedFormat}>
                            <option  value="" disabled>
                                Select Format
                            </option>
                            {['pdf', 'epub', 'doc', 'djvu', 'txt'].map((format) => (
                                <option key={format} value={format}>
                                    {format}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default BookInfoPage;

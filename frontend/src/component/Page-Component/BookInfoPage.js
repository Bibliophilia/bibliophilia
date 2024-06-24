import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';
import {useLocation, useNavigate} from 'react-router-dom';
import '../ComponentStyles/BookInfoPage.css'
import {BooksApi} from "../Component-APIs/BooksApi";
import {DEFAULT_COVER} from "../Utils/constants";
import {ReviewApi} from "../Component-APIs/ReviewApi";

const BookInfoPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const booksApi = new BooksApi();
    const reviewApi = new ReviewApi();
    const {idx} = useParams();

    const [bookInfo, setBookInfo] = useState(null);
    const [rating, setRating] = useState(0);
    const [reviews, setReviews] = useState([]);

    const [selectedFormat, setSelectedFormat] = useState('');
    const [isReadable, setIsReadable] = useState(false);
    const [error, setError] = useState(null);

    const [userRating, setUserRating] = useState("");
    const [userReview, setUserReview] = useState('');
    const [reviewResult, setReviewResult] = useState(null);

    useEffect(() => {
        const fetchBookInfo = async () => {
            booksApi.get(idx)
                .then(data => {
                    setBookInfo(data);
                    setIsReadable('pdf' in data.formats);
                })
                .catch(e => {
                    throw new Error(`HTTP error! ${e.toString()}`);
                });
            reviewApi.get_rating(idx)
                .then(data => {
                    setRating(data);
                })
                .catch(e => {
                    setRating(0);
                    console.log("Rating not found");
                })
            reviewApi.get_reviews(idx, 1)
                .then(data => {
                    setReviews(data);
                })
                .catch(e => {
                    setReviews([]);
                })
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
        window.location.href = `http://localhost:8000/books/download/?idx=${idx}&book_format=${selectedFormat}`;
    };

    const handleFormatSelect = (e) => {
        setSelectedFormat(e.target.value);
    };
    const handleRatingChange = (e) => {
        setUserRating(e.target.value);
        console.log(reviews);
    };
    const handleReviewChange = (e) => {
        setUserReview(e.target.value);
    };
    const handleSubmitReview = () => {
        const review = {
            "rating": Number(userRating),
            "review": userReview,
            "book_idx": idx,
            "user_idx": "default"
        }
        reviewApi.post_review(idx, review)
            .then(data => {
                setReviewResult("Review saved");
            })
            .catch(e => {
                setReviewResult("Oops! Review not saved!");
            });
    };
    const navigateToHome = () => {
        navigate('/');
    };

    return (
        <div className="Book-info-page-container">
            <div className="SP-header" onClick={navigateToHome}>
                <h1 className="SP-page-title">Bibliophilia</h1>
            </div>
            {error ? (
                <p>{error}</p>
            ) : bookInfo ? (
                <div className="book-page-wrapper">
                    <div className="book-container">
                        <div className="book-files-container">
                            <img className="book-cover-img"
                                 src={bookInfo.image_url} alt={bookInfo.title}
                                 onError={({currentTarget}) => {
                                     currentTarget.onerror = null;
                                     currentTarget.src = DEFAULT_COVER;
                                 }}/>
                            <button className="read-now-button" disabled={!isReadable} onClick={handleReadOnline}>Read
                                Now
                            </button>
                            <div className="book-download-container">
                                <button className="download-button" disabled={(!selectedFormat)}
                                        onClick={handleDownload}>Download
                                </button>
                                <select className="dropdown-box-bookinfo" onChange={handleFormatSelect}
                                        value={selectedFormat}>
                                    <option value="" disabled> Select Format</option>
                                    {bookInfo.formats.map((format) => (
                                        <option value={format}> {format} </option>
                                    ))}
                                </select>
                            </div>
                        </div>
                        <div className="book-info-container">
                            <div className="card-title">
                                <h2 className="book-title-bookinfo">{bookInfo.title}</h2>
                                <p className="rating-text">{'★'.repeat(rating)}</p>
                            </div>
                            <p className="book-author-bookinfo">{bookInfo.author.join(", ")}</p>
                            <p className="book-year-bookinfo">{bookInfo.year}</p>
                            <p className="book-genre-bookinfo">{bookInfo.genre.join(", ")}</p>
                            <p className="book-description-bookinfo">{bookInfo.description}</p>
                        </div>
                    </div>
                    <div className="book-review-container">
                        <h2 className="review-book-title"> Reviews </h2>
                        <div className="reviews">
                            {reviews.map((review_data) => (
                                <div className="review-card">
                                    <div className="card-title">
                                        <h3 className="username-text">{review_data.username}</h3>
                                        <p className="rating-text">{'★'.repeat(review_data.rating)}</p>
                                    </div>
                                    <p className="review-text">{review_data.review}</p>
                                </div>
                            ))}
                        </div>
                        <div className="review-edit-container">
                            {reviewResult ? (
                                <p>{reviewResult}</p>
                            ) : (
                                <div className="review-card">
                                    <div className="card-title">
                                        <h3 className="username-text">Rate the book!</h3>
                                        <div className="star-rating">
                                            <select className="rating" onChange={handleRatingChange}
                                                    value={userRating}>
                                                <option value="" disabled>Select a rating</option>
                                                {[5, 4, 3, 2, 1].map((number) => (
                                                    <option value={number}> {number} </option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>
                                    <textarea className="description" onChange={handleReviewChange}/>
                                    <div className="review-button-container">
                                        <div></div>
                                        <button className="review-button" onClick={handleSubmitReview}> Send</button>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default BookInfoPage;

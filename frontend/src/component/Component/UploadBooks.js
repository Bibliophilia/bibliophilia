import React, {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom'; // Import useNavigate instead of useHistory
import '../ComponentStyles/UploadBook.css';
import {BooksApi} from "../Component-APIs/BooksApi";

const UploadBooks = () => {
        const navigate = useNavigate(); // Change from useHistory to useNavigate
        const booksApi = new BooksApi();
        const re = /\s*(?:,|$)\s*/;
        const initialFormData = {
            bookTitle: '',
            author: '',
            year: 2024,
            genre: '',
            description: '',
            bookFiles: [],
            coverPhoto: null,
            coverPhotoURL: '',
        };
        const [formData, setFormData] = useState(initialFormData);
        const [error, setError] = useState(null);
        const [success, setSuccess] = useState(false);
        const handleChange = (e) => {
            const {name, value} = e.target;
            setFormData((prevData) => ({
                ...prevData,
                [name]: value,
            }));
        };
        const isValidFormat = (file, formats) => {
            const fileFormat = file.name.split('.').pop().toLowerCase();
            return formats.includes(fileFormat);
        }
        const handleImageChange = async (e) => {
            const files = e.target.files;
            const allowedFormats = ['jpg'];
            const file = files[0];
            if (!isValidFormat(file, allowedFormats)) {
                setError('Incorrect file format for cover photo. Please select a JPG file.');
                return;
            }
            setFormData((prevData) => ({
                ...prevData,
                'coverPhoto': file,
                }));
            const reader = new FileReader();
            reader.onloadend = () => {
                setFormData((prevData) => ({
                    ...prevData,
                    coverPhotoURL: reader.result,
                }));
            };
            await new Promise((resolve) => {
                reader.readAsDataURL(file);
                reader.onloadend = resolve;
            });
            setError(null);
        }
        const handleFileChange = async (e) => {
            const files = e.target.files;
            const allowedFormats = ['txt', 'doc', 'docx', 'pdf', 'epub', 'djvu'];
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                if (!isValidFormat(file, allowedFormats)) {
                    setError('Incorrect file format for book file(s). Please select files with formats: TXT, DOC, DOCX, PDF, EPUB, DJVU.');
                    return;
                }
            }
            setFormData((prevData) => ({
                ...prevData,
                'bookFiles': files,
                }));
            setError(null);
        };
        const clearForm = () => {
            setFormData(initialFormData);
            const coverPhotoInput = document.getElementById('coverPhotoInput');
            const bookFilesInput = document.getElementById('bookFilesInput');
            if (coverPhotoInput) {
                coverPhotoInput.value = null;
            }
            if (bookFilesInput) {
                bookFilesInput.value = null;
            }
        };
        const handleSubmit = async (e) => {
            e.preventDefault();
            const book = {
                "title": formData.bookTitle.toString(),
                "year": Number(formData.year),
                "description": formData.description.toString(),
                "author": formData.author.split(re),
                "genre": formData.genre.split(re)
            }

            console.log(book)
            booksApi.upload(book)
                .then(idx => {
                    console.log(`Book ${idx} uploaded. Uploading files...`);
                    booksApi.upload_cover(idx, formData.coverPhoto)
                        .then(data => {
                            console.log("Image uploaded successfully.");
                        })
                        .catch(error => {
                            console.error('An error occurred:', error.toString());
                            setError('An error occurred while uploading cover.');
                        });
                    for (let i = 0; i < formData.bookFiles.length; i++) {
                        booksApi.upload_file(idx, formData.bookFiles[i])
                            .then(data=>{
                                console.log(`File ${formData.bookFiles[i].name} uploaded successfully.`);
                            })
                            .catch(error => {
                                console.error('An error occurred:', error.toString());
                                setError('An error occurred while uploading book file.');
                            });
                    }
                    //clearForm();
                })
                .catch(error => {
                    console.error('An error occurred:', error.toString());
                    setError('An error occurred while processing your request.');
                });

        };

        useEffect(() => {
            if (success) {
                const timer = setTimeout(() => {
                    setSuccess(false);
                }, 5000); // Display success message for 5 seconds
                return () => clearTimeout(timer);
            }
        }, [success]);

        const handleCoverPhotoPreview = (e) => {
            const file = e.target.files[0];

            if (file) {
                const reader = new FileReader();
                reader.onloadend = () => {
                    setFormData((prevData) => ({
                        ...prevData,
                        coverPhotoURL: reader.result,
                    }));
                };

                reader.readAsDataURL(file);
            }
        };

        // Function to navigate to the home page
        const navigateToHome = () => {
            // Replace the path with the route to your home page
            navigate('/');
        };


        return (
            <div className="upload-books-page">
                <div className="Up-bar-for-title" onClick={navigateToHome}>
                    <h1 className="page-title">Bibliophilia</h1>
                </div>

                <h2 className="Header-upload-book">Share your Books with the world!</h2>

                <div className="Upload-book-container">
                    {success && <div className="success-message">Book uploaded successfully!</div>}
                    {error && <div className="error-message">{error}</div>}

                    <form onSubmit={handleSubmit}>
                        <div className="book-details-part">
                            <div className="book-details-right">
                                <label className="book-title">
                                    Book Title:
                                    <input
                                        type="text"
                                        name="bookTitle"
                                        value={formData.bookTitle}
                                        onChange={handleChange}
                                    />
                                </label>

                                <label className="author">
                                    Author:
                                    <input
                                        type="text"
                                        name="author"
                                        value={formData.author}
                                        onChange={handleChange}
                                        list={"list"}
                                    />
                                </label>
                                <label className="year">
                                    Year:
                                    <input
                                        type="number"
                                        defaultValue={formData.year}
                                        name="year"
                                        value={formData.year}
                                        onChange={handleChange}
                                        inputMode={"numeric"}
                                    />
                                </label>
                                <label className="genre">
                                    Genres:
                                    <input
                                        type="text"
                                        defaultValue={formData.genre}
                                        name="genre"
                                        value={formData.genre}
                                        onChange={handleChange}/>
                                </label>

                                <label className="description">
                                    Description:
                                    <textarea
                                        name="description"
                                        value={formData.description}
                                        onChange={handleChange}
                                    />
                                </label>
                            </div>
                        </div>

                        <div className="file-uploading-part">
                            <div className="file-uploading-left">
                                {formData.coverPhotoURL && (
                                    <div>
                                        <img
                                            src={formData.coverPhotoURL}
                                            alt="Cover Preview"
                                            className="cover-preview"
                                        />
                                        <br/>
                                    </div>
                                )}

                                <label className="choose-cover-photo">
                                    Choose a cover photo :
                                    <input
                                        id="coverPhotoInput"
                                        type="file"
                                        accept=".jpg, .jpeg, .png"
                                        onChange={(e) => {
                                            handleImageChange(e);
                                            handleCoverPhotoPreview(e); // Add this line to update cover photo preview
                                        }}
                                    />
                                </label>

                                <br/>

                                <label className="choose-book-file">
                                    Choose book files :
                                    <input
                                        id="bookFilesInput"
                                        type="file"
                                        accept=".txt, .doc, .docx, .pdf, .epub, .djvu"
                                        onChange={(e) => handleFileChange(e)}
                                        multiple
                                    />
                                </label>
                            </div>
                        </div>

                        <button className="submit-books" type="submit">
                            Upload
                        </button>
                    </form>
                </div>
            </div>
        );
    }
;

export default UploadBooks;

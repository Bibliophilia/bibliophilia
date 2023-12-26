import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory
import './ComponentStyles/UploadBook.css';

const UploadBooks = () => {
  const navigate = useNavigate(); // Change from useHistory to useNavigate

  const initialFormData = {
    bookTitle: '',
    author: '',
    description: '',
    bookFiles: [],
    coverPhoto: null,
    coverPhotoURL: '',
  };

  const [formData, setFormData] = useState(initialFormData);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleFileChange = async (e, fileType) => {
    const files = e.target.files;

    // Check file format and set preview for cover photo
    if (fileType === 'coverPhoto' && files.length > 0) {
      const file = files[0];
      const allowedFormats = ['jpg', 'jpeg', 'png'];
      const fileFormat = file.name.split('.').pop().toLowerCase();

      if (allowedFormats.includes(fileFormat)) {
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
      } else {
        setError('Incorrect file format for cover photo. Please select a JPG, JPEG, or PNG file.');
        return;
      }
      setFormData((prevData) => ({
      ...prevData,
      'coverPhoto': file,
    }));
    }

    // Check file formats for book files
    if (fileType === 'bookFiles') {
      const allowedFormats = ['txt', 'doc', 'docx', 'pdf', 'epub', 'djvu'];

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileFormat = file.name.split('.').pop().toLowerCase();

        if (!allowedFormats.includes(fileFormat)) {
          setError('Incorrect file format for book file(s). Please select files with formats: TXT, DOC, DOCX, PDF, EPUB, DJVU.');
          return;
        }
      }
      setFormData((prevData) => ({
      ...prevData,
      'bookFiles': files,
    }));
    }

    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const requestData = new FormData();

      // Create a File object for image_file
      requestData.append('image_file', formData.coverPhoto);

      // Append only image_file and files to FormData
      for (let i = 0; i < formData.bookFiles.length; i++) {
        requestData.append(`files`, formData.bookFiles[i]);
      }

      const queryParams = `?title=${encodeURIComponent(formData.bookTitle)}&author=${encodeURIComponent(formData.author)}&description=${encodeURIComponent(formData.description)}`;
      const url = `http://localhost:8000/books/upload${queryParams}`;

      const response = await fetch(url, {
        method: 'POST',
        body: requestData,
      });

      if (response.ok) {
        console.log('Books uploaded successfully');
        setSuccess(true);
        // Clear form data after successful upload
        setFormData(initialFormData);

        // Reset file input fields
        const coverPhotoInput = document.getElementById('coverPhotoInput');
        const bookFilesInput = document.getElementById('bookFilesInput');

        if (coverPhotoInput) {
          coverPhotoInput.value = null;
        }

        if (bookFilesInput) {
          bookFilesInput.value = null;
        }
      } else {
        const responseText = await response.text();
        console.error('Error response:', responseText);
        setError('An error occurred while processing your request.');
      }
    } catch (error) {
      console.error('An error occurred:', error);
      setError('An error occurred while processing your request.');
    }
  };

  useEffect(() => {
    if (success) {
      const timer = setTimeout(() => {
        setSuccess(false);
      }, 5000); // Display success message for 5 seconds
      return () => clearTimeout(timer);
    }
  }, [success]);

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

        <h2 className="Header-upload-book">Upload your Books!</h2>

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
                  />
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
                      <br />
                    </div>
                )}

                <label className="choose-cover-photo">
                  Choose a cover photo :
                  <input
                      id="coverPhotoInput"
                      type="file"
                      accept=".jpg, .jpeg, .png"
                      onChange={(e) => handleFileChange(e, 'coverPhoto')}
                  />
                </label>

                <br />

                <label className="choose-book-file">
                  Choose book files :
                  <input
                      id="bookFilesInput"
                      type="file"
                      accept=".txt, .doc, .docx, .pdf, .epub, .djvu"
                      onChange={(e) => handleFileChange(e, 'bookFiles')}
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
};

export default UploadBooks;

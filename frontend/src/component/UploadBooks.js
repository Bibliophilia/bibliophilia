import React, { useState } from 'react';
import './ComponentStyles/UploadBook.css';

const UploadBooks = () => {
  const [formData, setFormData] = useState({
    bookTitle: '',
    author: '',
    description: '',
    bookFiles: [],
    coverPhoto: null,
    coverPhotoURL: '',
  });

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

    setFormData((prevData) => ({
      ...prevData,
      [fileType]: files,
    }));

    if (fileType === 'coverPhoto' && files.length > 0) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData((prevData) => ({
          ...prevData,
          coverPhotoURL: reader.result,
        }));
      };

      await new Promise((resolve) => {
        reader.readAsDataURL(files[0]);
        reader.onloadend = resolve;
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const requestData = new FormData();

      // Create a File object for image_file
      const coverPhotoFile = new File([formData.coverPhoto], formData.coverPhoto.name);
      requestData.append('image_file', coverPhotoFile);

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
        setFormData({
          bookTitle: '',
          author: '',
          description: '',
          bookFiles: [],
          coverPhoto: null,
          coverPhotoURL: '',
        });
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

  return (
      <div className="upload-books-page">
        <div className='Up-bar-for-title'>
          <h1 className='page-title'>Bibliophilia</h1>
        </div>

        <h2 className='Header'>Upload your Books!</h2>

        <div className='Upload-book-container'>
          {success && (
              <div className="success-message">
                Book uploaded successfully!
              </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className='book-details-part'>
              <div className='book-details-right'>
                <label className='book-title'>
                  Book Title:
                  <input
                      type="text"
                      name="bookTitle"
                      value={formData.bookTitle}
                      onChange={handleChange}
                  />
                </label>

                <label className='author'>
                  Author:
                  <input
                      type="text"
                      name="author"
                      value={formData.author}
                      onChange={handleChange}
                  />
                </label>

                <label className='description'>
                  Description:
                  <textarea
                      name="description"
                      value={formData.description}
                      onChange={handleChange}
                  />
                </label>
              </div>
            </div>

            <div className='file-uploading-part'>
              <div className='file-uploading-left'>
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

                <label className='choose-cover-photo'>
                  Choose a cover photo:
                  <input type="file" onChange={(e) => handleFileChange(e, 'coverPhoto')} />
                </label>

                <br />

                <label className='choose-book-file'>
                  Choose book files:
                  <input type="file" onChange={(e) => handleFileChange(e, 'bookFiles')} multiple />
                </label>
              </div>
            </div>

            <button className='submit-books' type="submit">Upload</button>
          </form>
        </div>
      </div>
  );
};

export default UploadBooks;

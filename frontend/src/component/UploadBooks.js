import React, { useState } from 'react';
import './ComponentStyles/UploadBook.css';

const UploadBooks = () => {
  const [formData, setFormData] = useState({
    bookTitle: '',
    author: '',
    description: '',
    bookFiles: [],
    coverPhoto: null,
    coverPhotoURL: '', // To store the cover photo URL
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleFileChange = (e, fileType) => {
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
      reader.readAsDataURL(files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const requestData = new FormData();
      requestData.append('title', formData.bookTitle);
      requestData.append('author', formData.author);
      requestData.append('description', formData.description);
      requestData.append('image_file', formData.coverPhoto);

      for (let i = 0; i < formData.bookFiles.length; i++) {
        requestData.append('files', formData.bookFiles[i]);
      }

      const response = await fetch('http://localhost:8000/books/upload', {
        method: 'POST',
        body: requestData,
      });

      if (response.ok) {
        console.log('Books uploaded successfully');
        // Reset form data after successful upload
        setFormData({
          bookTitle: '',
          author: '',
          description: '',
          bookFiles: [],
          coverPhoto: null,
          coverPhotoURL: '',
        });
      } else {
        console.error('Failed to upload books. Server returned:', response.status);

        const responseText = await response.text();
        console.error('Server response:', responseText);

        try {
          const responseData = JSON.parse(responseText);
          console.error('Validation errors:', responseData.detail);
        } catch (parseError) {
          console.error('Failed to parse response JSON:', parseError);
        }
      }
    } catch (error) {
      console.error('An error occurred:', error);
    }
  };


  return (
      <div className="upload-books-page">
        <div className='Up-bar-for-title'>
          <h1 className='page-title'>Bibliophilia</h1>
        </div>

        <h2 className='Header'>Upload your Books!</h2>

        <div className='Upload-book-container'>
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

                {/*

                <label className='genre'>
                  Genre:
                  <input
                      type="text"
                      name="genre"
                      value={formData.genre}
                      onChange={handleChange}
                  />
                </label>
                 */}

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
                    <img
                        src={formData.coverPhotoURL}
                        alt="Cover Preview"
                        className="cover-preview"
                    />
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

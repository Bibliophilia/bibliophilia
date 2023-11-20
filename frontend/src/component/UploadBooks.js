import React, { useState } from 'react';
import './ComponentStyles/UploadBook.css';

const UploadBooks = () => {
  const [formData, setFormData] = useState({
    bookTitle: '',
    author: '',
    genre: '',
    description: '',
    bookFile: null,
    coverPhoto: null,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleFileChange = (e, fileType) => {
    const file = e.target.files[0];

    setFormData((prevData) => ({
      ...prevData,
      [fileType]: file,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Perform the book upload logic here, for example, making a request to the backend
    console.log('Book Title:', formData.bookTitle);
    console.log('Author:', formData.author);
    console.log('Genre:', formData.genre);
    console.log('Description:', formData.description);
    console.log('Book File:', formData.bookFile);
    console.log('Cover Photo:', formData.coverPhoto);

    // Clear form fields after submission
    setFormData({
      bookTitle: '',
      author: '',
      genre: '',
      description: '',
      bookFile: null,
      coverPhoto: null,
    });
  };

  return (
    <div className="upload-books-page">
      <div className='Up-bar-for-title'>
        <h1 className='page-title'>Bibliophilia</h1>
      </div>

      <h2 className='Header'>Upload your Books!</h2>

      <form onSubmit={handleSubmit}>
        <div className='book-details-part'>
          <label className='book-title'>
            Book Title:
            <input
              type="text"
              name="bookTitle"
              value={formData.bookTitle}
              onChange={handleChange}
            />
          </label>
          <br />
          <label className='author'>
            Author:
            <input
              type="text"
              name="author"
              value={formData.author}
              onChange={handleChange}
            />
          </label>
          <br />
          <label className='genre'>
            Genre:
            <input
              type="text"
              name="genre"
              value={formData.genre}
              onChange={handleChange}
            />
          </label>
          <br />
          <label className='description'>
            Description:
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
            />
          </label>
        </div>

        <div className='file-uploading-part'>
          {/* to Display the uploaded cover image */}
          {formData.coverPhoto && (
            <img
              src={URL.createObjectURL(formData.coverPhoto)}
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
            Choose a book file:
            <input type="file" onChange={(e) => handleFileChange(e, 'bookFile')} />
          </label>
        </div>

        <br />
        <button className='submit-books' type="submit">Upload</button>
      </form>
    </div>
  );
};

export default UploadBooks;

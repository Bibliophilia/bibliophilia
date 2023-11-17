import React, { useState } from 'react';

const UploadBooks = () => {
  const [bookTitle, setBookTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState(null);

  const handleTitleChange = (e) => {
    setBookTitle(e.target.value);
  };

  const handleAuthorChange = (e) => {
    setAuthor(e.target.value);
  };

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleFileChange = (e) => {
    // Assuming you want to handle file uploads, save the file in state
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Perform the book upload logic here, for example, making a request to the backend

    console.log('Book Title:', bookTitle);
    console.log('Author:', author);
    console.log('Description:', description);
    console.log('File:', file);

    // Clear form fields after submission
    setBookTitle('');
    setAuthor('');
    setDescription('');
    setFile(null);
  };

  return (
    <div>
      <h2>Upload Books</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Book Title:
          <input type="text" value={bookTitle} onChange={handleTitleChange} />
        </label>
        <br />
        <label>
          Author:
          <input type="text" value={author} onChange={handleAuthorChange} />
        </label>
        <br />
        <label>
          Description:
          <textarea value={description} onChange={handleDescriptionChange} />
        </label>
        <br />
        <label>
          Choose a file:
          <input type="file" onChange={handleFileChange} />
        </label>
        <br />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
};

export default UploadBooks;

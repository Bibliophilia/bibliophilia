import { HttpApi } from "component/Component-APIs/HttpApi";
import { SERVER_URL } from 'component/Utils/constants';

export class BooksApi extends HttpApi {
  constructor() {
    super(SERVER_URL + '/books');
  }

  upload(book) {
    //const queryParams = `?title=${encodeURIComponent(book.title)}` +
    //    `&year=${encodeURIComponent(book.year)}` +
    //    `&publisher=${encodeURIComponent(book.publisher)}` +
    //    `&description=${encodeURIComponent(book.description)}` +
    //    `&author=${encodeURIComponent(book.author)}` +
    //    `&genre=${encodeURIComponent(book.genre)}`;
    console.log(document.cookie)
    return this.sendRequest(`/data/upload/`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type' : 'application/json'},
      body: JSON.stringify(book)
    });
  }
  upload_cover(idx, image) {
    const formData = new FormData();
    formData.append('image', image);

    return this.sendRequest(`/image/upload?book_idx=${idx}`, {
      method: 'POST',
      body: formData
    });
  }
  upload_file(idx, file) {
    const formData = new FormData();
    formData.append('file', file);
    return this.sendRequest(`/file/upload?book_idx=${idx}`, {
      method: 'POST',
      body: formData
    });
  }
}

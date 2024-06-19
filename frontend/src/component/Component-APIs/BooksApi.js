import { HttpApi } from "component/Component-APIs/HttpApi";
import { SERVER_URL } from 'component/Utils/constants';

export class BooksApi extends HttpApi {
  constructor() {
    super(SERVER_URL + '/books');
  }

  upload(book) {
    const queryParams = `?title=${encodeURIComponent(book.title)}` +
        `&year=${encodeURIComponent(book.year)}` +
        `&publisher=${encodeURIComponent(book.publisher)}` +
        `&description=${encodeURIComponent(book.description)}` +
        `&author=${encodeURIComponent(book.author)}` +
        `&genre=${encodeURIComponent(book.genre)}`;
    return this.sendRequest(`/data/upload${queryParams}`,{}, {
      method: 'GET',
      headers: { 'accept': 'application/json' }
    });
  }
  upload_cover(idx, image) {
    const formData = new FormData();
    formData.append('image', image);

    return this.sendRequest(`/image/upload?idx=${idx}`, {
      method: 'POST',
      body: formData
    });
  }
  upload_file(idx, file) {
    const formData = new FormData();
    formData.append('file', file);
    return this.sendRequest(`/file/upload?idx=${idx}`, {
      method: 'POST',
      body: formData
    });
  }
}

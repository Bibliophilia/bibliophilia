import { HttpApi } from "component/Component-APIs/HttpApi";
import { SERVER_URL } from 'component/Utils/constants';

export class BooksApi extends HttpApi {
  constructor() {
    super(SERVER_URL + '/books');
  }

  upload(book) {
    return this.sendRequest(`/data/upload`, {
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
      credentials: 'include',
      body: formData
    });
  }
  upload_file(idx, file) {
    const formData = new FormData();
    formData.append('file', file);
    return this.sendRequest(`/file/upload?book_idx=${idx}`, {
      method: 'POST',
      credentials: 'include',
      body: formData
    });
  }
  get(idx){
    return this.sendRequest(`/${idx}`, {
      method: 'GET',
      credentials: 'include'
    });
  }
  add_rights(idx, user_idx, rights){
    return this.sendRequest(`/books/add-rights?book_idx=${idx}$user_idx=${user_idx}`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type' : 'application/json'},
      body: JSON.stringify(rights)
    });
  }
}

import {HttpApi} from "./HttpApi";
import {SERVER_URL} from "../Utils/constants";

export class ReviewApi extends HttpApi {
  constructor() {
    super(SERVER_URL + '/users/review');
  }

  get_rating(idx){
    return this.sendRequest(`/rating/${idx}`, {
      method: 'GET'
    });
  }
  get_reviews(idx, page){
    return this.sendRequest(`/?book_idx=${idx}&page=${page}`, {
      method: 'GET'
    });
  }
  post_review(idx, review){
    return this.sendRequest(`/upload`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type' : 'application/json'},
      body: JSON.stringify(review)
    });
  }
}
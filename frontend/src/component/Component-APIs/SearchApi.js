import {HttpApi} from "component/Component-APIs/HttpApi";
import { SERVER_URL } from 'component/Utils/constants';

export class SearchApi extends HttpApi{
  constructor() {
    super(SERVER_URL+'/books/search');
  }
    search(query, page){
        return this.sendRequest(`/?q=${query}&page=${page}`,{
            method: 'GET',
            headers: { 'accept': 'application/json' }
        })
    }

    getFacets(){
        return this.sendRequest(`/facets`,{
            method: 'GET',
            headers: { 'accept': 'application/json' }
        })
    }
    getHints(facet, query){
        return this.sendRequest(`/hints?q=${query}&facet=${facet}`,{
            method: 'GET',
            headers: { 'accept': 'application/json' }
        });
    }
}

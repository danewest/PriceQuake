import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PriceService {

  constructor(private http: HttpClient) {}

  getPrices(ticker: string): Observable<any> {
    // This will later become your backend API URL
    return this.http.get(`assets/mock/prices-${ticker}.json`);
  }
}

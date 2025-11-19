import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FundamentalsService {

  constructor(private http: HttpClient) {}

  getFundamentals(ticker: string): Observable<any> {
    return this.http.get(`assets/mock/fundamentals-${ticker}.json`);
  }
}

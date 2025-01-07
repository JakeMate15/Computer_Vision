import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ValidationService {
  constructor(private http: HttpClient) {}

  validateCards(card1: string, card2: string): Observable<Boolean> {
    return this.http.post<boolean>('http://localhost:5000/api/validate', {
      card1, 
      card2
    })
  }
}
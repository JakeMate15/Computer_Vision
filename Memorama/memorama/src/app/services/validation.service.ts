import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs'

interface ValidationResponse {
  valid: boolean
}

@Injectable({
  providedIn: 'root'
})
export class ValidationService {
  private apiUrl = 'http://localhost:5000/api/validate'

  constructor(private http: HttpClient) {}

  validateCards(card1: string, card2: string): Observable<ValidationResponse> {
    return this.http.post<ValidationResponse>(this.apiUrl, { card1, card2 })
  }
}

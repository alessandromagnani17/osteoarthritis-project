import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:3000/api/users/register';

  constructor(private http: HttpClient) { }

  register(userData: { username: string, password: string }): Observable<any> {
    return this.http.post(this.apiUrl, userData);
  }
}

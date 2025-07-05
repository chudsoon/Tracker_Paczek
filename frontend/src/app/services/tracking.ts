import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

//serwis dostępny globalnie w aplikacji

@Injectable({
  providedIn: 'root'
})
export class Tracking {
  private apiUrl = 'http://localhost:8000/trackings'; // adres backendu FastAPI

  constructor(private http: HttpClient) { }

  //pobiera listę przesyłek dla danego uzytkownika
  getTrackings(userId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/?user_id=${userId}`)
  }
  //dodaje nową przesyłkę
  addTracking(data: {number: string; carrier: string, user_id: number}) {
    return this.http.post(this.apiUrl, data)
  }
}

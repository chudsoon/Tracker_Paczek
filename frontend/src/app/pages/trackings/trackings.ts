import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ColdObservable } from 'rxjs/internal/testing/ColdObservable';
import { Tracking } from '../../services/tracking';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-trackings',
  standalone: true ,
  imports: [CommonModule, FormsModule],
  templateUrl: './trackings.html',
  styleUrl: './trackings.css'
})
export class Trackings implements OnInit {
  trackings: any[] = []; //tablica przesyłek
  newTracking = { number: '', carrier: ''}; // dane z formularza

  constructor(private tracking: Tracking) {}

  ngOnInit(): void {
    this.loadTrackings();
  }

  //pobieramy dane z backendu przez serwis
  loadTrackings(): void {
    this.tracking.getTrackings(1).subscribe({
      next: (data) => this.trackings = data,
      error: (err) => console.error('Błąd pobierania przesyłek:', err)
    });
  }

  //wysyła przesyłkę do backendu (POST)
  addTracking(): void {
    const payload = {
      ...this.newTracking,
      user_id: 1 // na razie na szytwno - później dynamicznie

    };
    
    this.tracking.addTracking(payload).subscribe({
      next: () => {
        this.newTracking = { number: '', carrier: ''}; //wyszczyść formularz
        this.loadTrackings();
      }
    })
  }

}

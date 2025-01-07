import { Component } from '@angular/core'
import { Router } from '@angular/router'
import { CommonModule } from '@angular/common' // para ngIf, ngFor
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  constructor(private router: Router) {}

  startGame(cardsCount: number) {
    this.router.navigate(['/game', cardsCount])
  }
}

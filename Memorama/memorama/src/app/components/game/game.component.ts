import { Component, OnInit } from '@angular/core'
import { ActivatedRoute } from '@angular/router'
import { CommonModule } from '@angular/common'
import { ScoreboardComponent } from '../scoreboard/scoreboard.component'
import { ValidationService } from '../../services/validation.service'
import { Card } from '../../models/card'
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs'
import { map, catchError } from 'rxjs/operators'

interface Pair {
  images: string[]
}

interface PairsData {
  pairs: Pair[]
}

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [CommonModule, ScoreboardComponent],
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {
  cards: Card[] = []
  selectedCards: Card[] = []
  reversoImg = 'assets/reverso.png'
  totalCards = 0
  currentPlayer = 1
  player1Score = 0
  player2Score = 0
  allPairs: Pair[] = []
  gameEnded = false

  constructor(
    private route: ActivatedRoute,
    private validationService: ValidationService,
    private http: HttpClient
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.totalCards = +params['cardsCount']
      if (this.totalCards % 2 !== 0) {
        alert('El número de cartas debe ser par.')
        return
      }
      this.loadPairs().subscribe(() => {
        this.loadCards()
        // Eliminado: this.startGameTimer()
      })
    })
  }

  loadPairs(): Observable<void> {
    return this.http.get<PairsData>('assets/images/pairs.json').pipe(
      map(data => {
        this.allPairs = data.pairs
      }),
      catchError(error => {
        console.error('Error al cargar pairs.json:', error)
        alert('No se pudieron cargar las parejas de cartas.')
        throw error
      })
    )
  }

  loadCards() {
    const numberOfPairs = this.totalCards / 2
    if (numberOfPairs > this.allPairs.length) {
      alert('No hay suficientes parejas en el archivo JSON para el número de cartas seleccionadas.')
      return
    }
    const selectedPairs = this.shuffleArray<Pair>([...this.allPairs]).slice(0, numberOfPairs)
    const temp: Card[] = []
    selectedPairs.forEach((pair: Pair, index: number) => {
      pair.images.forEach((image: string) => {
        temp.push({
          id: index * 2 + temp.length,
          image: `assets/images/${image}`,
          flipped: false,
          matched: false
        })
      })
    })
    this.cards = this.shuffleArray<Card>(temp)
  }

  shuffleArray<T>(array: T[]): T[] {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[array[i], array[j]] = [array[j], array[i]]
    }
    return array
  }

  selectCard(card: Card) {
    if (card.flipped || this.selectedCards.length === 2 || this.gameEnded) {
      return
    }
    card.flipped = true
    this.selectedCards.push(card)

    if (this.selectedCards.length === 2) {
      const card1 = this.selectedCards[0].image
      const card2 = this.selectedCards[1].image

      this.validationService.validateCards(card1, card2).subscribe(
        response => {
          const valid = response.valid
          const selected1 = this.selectedCards[0]
          const selected2 = this.selectedCards[1]

          if (valid) {
            selected1.matched = true
            selected2.matched = true
            this.addPoint()
          } else {
            setTimeout(() => {
              selected1.flipped = false
              selected2.flipped = false
            }, 1000)
          }
          this.selectedCards = []
          this.changePlayer()
          this.checkGameEnd()
        },
        error => {
          console.error('Error en la validación de las cartas:', error)
          alert('Ocurrió un error al validar las cartas. Por favor, intenta de nuevo.')
        }
      )
    }
  }

  addPoint() {
    if (this.currentPlayer === 1) {
      this.player1Score++
    } else {
      this.player2Score++
    }
  }

  changePlayer() {
    this.currentPlayer = this.currentPlayer === 1 ? 2 : 1
  }

  checkGameEnd() {
    const allMatched = this.cards.every(card => card.matched)
    if (allMatched) {
      this.gameEnded = true
      this.showWinner()
    }
  }

  showWinner() {
    let message = 'Fin del juego.\n'
    if (this.player1Score > this.player2Score) {
      message += 'Jugador 1 es el ganador!'
    } else if (this.player2Score > this.player1Score) {
      message += 'Jugador 2 es el ganador!'
    } else {
      message += 'Es un empate!'
    }
    const playAgain = confirm(`${message}\n¿Quieres jugar de nuevo?`)
    if (playAgain) {
      this.resetGame()
    } else {
      alert('Gracias por jugar!')
    }
  }

  resetGame() {
    this.cards = []
    this.selectedCards = []
    this.currentPlayer = 1
    this.player1Score = 0
    this.player2Score = 0
    this.gameEnded = false
    this.loadCards()
    // Eliminado:
    // clearInterval(this.intervalId)
    // this.startGameTimer()
  }
}

import { Component, OnInit } from '@angular/core'
import { ActivatedRoute } from '@angular/router'
import { HttpClient } from '@angular/common/http'
import { ValidationService } from '../../services/validation.service'
import { Card } from '../../models/card'
import { CommonModule, NgIf, NgFor } from '@angular/common'
import { ScoreboardComponent } from '../scoreboard/scoreboard.component'
import { TimerComponent } from '../timer/timer.component'

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [
    CommonModule,
    NgIf,
    NgFor,
    ScoreboardComponent,
    TimerComponent
  ],
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
  timePerTurn = 10
  gameDuration = 120
  intervalId: any
  timerCount = 0

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private validationService: ValidationService
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.totalCards = +params['cardsCount']
      this.loadCards()
      this.startGameTimer()
    })
  }

  loadCards() {
    const jsonPath = 'assets/images/pairs.json'
    this.http.get<{ pairs: { images: string[] }[] }>(jsonPath)
      .subscribe(data => {
        const totalPairs = this.totalCards / 2
        const selectedPairs = this.getRandomElements(data.pairs, totalPairs)

        const temp: Card[] = []
        let cardId = 0

        selectedPairs.forEach(pair => {
          pair.images.forEach(img => {
            temp.push({
              id: cardId++,
              image: `assets/images/${img}`,
              flipped: false,
              matched: false
            })
          })
        })

        this.cards = this.shuffleArray(temp)
      })
  }

  getRandomElements<T>(array: T[], n: number): T[] {
    const copy = [...array]
    const result: T[] = []
    while (n > 0 && copy.length) {
      const index = Math.floor(Math.random() * copy.length)
      result.push(copy.splice(index, 1)[0])
      n--
    }
    return result
  }

  shuffleArray(array: Card[]) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[array[i], array[j]] = [array[j], array[i]]
    }
    return array
  }

  selectCard(card: Card) {
    if (card.flipped || this.selectedCards.length === 2) {
      return
    }
    card.flipped = true
    this.selectedCards.push(card)
    if (this.selectedCards.length === 2) {
      this.validationService.validateCards(
        this.selectedCards[0].image,
        this.selectedCards[1].image
      ).subscribe(valid => {
        if (valid) {
          if (this.selectedCards[0].image === this.selectedCards[1].image) {
            this.selectedCards[0].matched = true
            this.selectedCards[1].matched = true
            this.addPoint()
          } else {
            setTimeout(() => {
              this.selectedCards[0].flipped = false
              this.selectedCards[1].flipped = false
            }, 1000)
          }
        } else {
          setTimeout(() => {
            this.selectedCards[0].flipped = false
            this.selectedCards[1].flipped = false
          }, 1000)
        }
        this.selectedCards = []
        this.changePlayer()
        this.checkGameEnd()
      })
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
      alert('Fin del juego')
    }
  }

  onTimeUp() {
    this.changePlayer()
    this.selectedCards.forEach(card => (card.flipped = false))
    this.selectedCards = []
  }

  startGameTimer() {
    this.intervalId = setInterval(() => {
      this.timerCount++
      if (this.timerCount >= this.gameDuration) {
        clearInterval(this.intervalId)
        alert('Tiempo de juego finalizado')
      }
    }, 1000)
  }
}

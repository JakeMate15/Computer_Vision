import { Component, OnInit } from '@angular/core'
import { ActivatedRoute } from '@angular/router'

import { Card } from '../../models/card'
import { ValidationService } from '../../services/validation.service'
import { CommonModule, NgFor, NgIf } from '@angular/common'
import { ScoreboardComponent } from '../scoreboard/scoreboard.component'
import { TimerComponent } from '../timer/timer.component'

@Component({
  selector: 'app-game',
  imports: [
    CommonModule,
    NgIf,
    NgFor,
    ScoreboardComponent,
    TimerComponent
  ],
  templateUrl: './game.component.html',
  styleUrl: './game.component.css'
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
    const imagesPath = `assets/images/${this.totalCards}`
    const temp: Card[] = []
    for (let i = 0; i < this.totalCards; i++) {
      temp.push({
        id: i,
        image: `${imagesPath}/img${i % (this.totalCards / 2)}.png`,
        flipped: false,
        matched: false
      })
    }
    this.cards = this.shuffleArray(temp)
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
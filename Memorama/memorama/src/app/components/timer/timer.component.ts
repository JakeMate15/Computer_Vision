import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-timer',
  imports: [],
  templateUrl: './timer.component.html',
  styleUrl: './timer.component.css'
})
export class TimerComponent implements OnInit, OnDestroy {
  @Input() seconds = 10
  @Output() timeUp = new EventEmitter<void>()
  currentTime = 0
  intervalId: any

  ngOnInit() {
    this.currentTime = this.seconds
    this.intervalId = setInterval(() => {
      this.currentTime--
      if (this.currentTime <= 0) {
        clearInterval(this.intervalId)
        this.timeUp.emit()
        this.currentTime = this.seconds
        this.start()
      }
    }, 1000)
  }

  ngOnDestroy() {
    clearInterval(this.intervalId)
  }

  start() {
    this.intervalId = setInterval(() => {
      this.currentTime--
      if (this.currentTime <= 0) {
        clearInterval(this.intervalId)
        this.timeUp.emit()
        this.currentTime = this.seconds
        this.start()
      }
    }, 1000)
  }
}

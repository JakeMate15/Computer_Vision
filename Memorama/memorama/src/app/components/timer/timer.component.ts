import { Component, Input, Output, EventEmitter, OnInit, OnDestroy } from '@angular/core'

@Component({
  selector: 'app-timer',
  standalone: true,
  imports: [],
  templateUrl: './timer.component.html',
  styleUrls: ['./timer.component.css']
})
export class TimerComponent implements OnInit, OnDestroy {
  @Input() seconds = 10
  @Output() timeUp = new EventEmitter<void>()
  currentTime = 0
  intervalId: any

  ngOnInit() {
    this.resetTimer()
  }

  ngOnDestroy() {
    clearInterval(this.intervalId)
  }

  resetTimer() {
    clearInterval(this.intervalId)
    this.currentTime = this.seconds
    this.intervalId = setInterval(() => {
      this.currentTime--
      if (this.currentTime <= 0) {
        clearInterval(this.intervalId)
        this.timeUp.emit()
      }
    }, 1000)
  }
}

package mp

import (
  "fmt"
  "time"
)

type MP3Player struct {
  stat int
  progress int
}

func (P *MP3Player) play(source string) {
  fmt.Println("playing mp3", source)

  P.progress = 0

  for P.progress < 100 {
    time.Sleep(100 * time.Millisecond)
    fmt.Print(".")
    P.progress += 10
  }

  fmt.Println("\nFinished playing", source)
}
